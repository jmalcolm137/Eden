#!/usr/bin/env python3
"""Assemble the small Eden boot initramfs.

The squashfs root lives on the ISO; the initramfs only needs the static
liveinit plus the storage/filesystem modules required to find and mount it.
"""

import os
import pathlib
import subprocess
import sys

ROOTS = [
    "sr_mod",
    "cdrom",
    "isofs",
    "loop",
    "squashfs",
    "overlay",
    "ata_piix",
    "ata_generic",
    "ahci",
    "libata",
    "scsi_mod",
    "sd_mod",
    "virtio",
    "virtio_ring",
    "virtio_pci",
    "virtio_blk",
    "usbcore",
    "usb_common",
    "xhci_hcd",
    "xhci_pci",
    "ehci_hcd",
    "ehci_pci",
    "ohci_hcd",
    "ohci_pci",
    "uhci_hcd",
    "usb_storage",
    "uas",
    "nvme",
    "nvme_core",
]


def main() -> int:
    if len(sys.argv) != 3:
        print("usage: mkinitramfs.py ROOT STAGING", file=sys.stderr)
        return 2
    root = pathlib.Path(sys.argv[1])
    staging = pathlib.Path(sys.argv[2])

    modbase = root / "usr/lib/modules"
    versions = [p for p in modbase.iterdir() if p.is_dir()]
    if not versions:
        print("no module tree", file=sys.stderr)
        return 1
    moddir = versions[0]
    deps: dict[str, list[str]] = {}
    with (moddir / "modules.dep").open() as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            mod, dlist = line.split(":", 1)
            deps[mod] = dlist.split()

    byname = {os.path.basename(m).split(".ko")[0]: m for m in deps}
    seen: set[str] = set()
    order: list[str] = []

    def visit(name: str) -> None:
        mod = byname.get(name)
        if mod is None or mod in seen:
            return
        seen.add(mod)
        for dep in deps[mod]:
            visit(os.path.basename(dep).split(".ko")[0])
        order.append(mod)

    for r in ROOTS:
        visit(r)

    modstage = staging / "modules"
    modstage.mkdir(parents=True, exist_ok=True)
    out = []
    for mod in order:
        src = moddir / mod
        if not src.exists():
            print(f"missing module: {src}", file=sys.stderr)
            continue
        rel = src.relative_to(moddir)
        dst = modstage / rel.with_suffix("")
        dst.parent.mkdir(parents=True, exist_ok=True)
        with dst.open("wb") as f:
            subprocess.run(["zstd", "-dc", str(src)], stdout=f, check=True)
        out.append("/modules/" + str(rel.with_suffix("")))

    (staging / "modules.order").write_text("\n".join(out) + "\n")
    total = sum(os.path.getsize(staging / p.lstrip("/")) for p in out)
    print(f"initramfs modules: {len(out)} ({total} bytes)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
