pkgname = "base-kernel"
pkgver = "0.2"
pkgrel = 0
depends = ["kmod", "openbsd", "util-linux"]
# paths that should result in kernel.d hooks being rerun
triggers = [
    "+/usr/lib/depmod.d",
    "+/usr/lib/firmware",
    "+/usr/lib/modules/*",
    "+/usr/share/initramfs-tools",
    "+/usr/src",
]
pkgdesc = "Common data and scripts for Linux kernels"
license = "custom:meta"
url = "https://chimera-linux.org"
# no tests
options = ["!check"]


def install(self):
    for f in ["kernel-root-detect", "run-kernel-d"]:
        self.install_file(
            self.files_path / "libexec" / f,
            "usr/lib/base-kernel",
            mode=0o755,
        )

    self.install_file(
        self.files_path / "modprobe.d/usb-load-ehci-first",
        "usr/lib/modprobe.d",
        name="usb-load-ehci-first.conf",
    )
    self.install_file(
        self.files_path / "modprobe.d/blacklist.conf", "usr/lib/modprobe.d"
    )

    self.install_file(
        self.files_path / "linux-version.sh",
        "usr/bin",
        mode=0o755,
        name="linux-version",
    )
    self.install_file(
        self.files_path / "chimera-buildkernel.sh",
        "usr/bin",
        mode=0o755,
        name="chimera-buildkernel",
    )
    self.install_file(
        self.files_path / "chimera-stripko.sh",
        "usr/bin",
        mode=0o755,
        name="chimera-stripko",
    )

    self.install_file(
        self.files_path / "49-depmod.sh", "usr/lib/kernel.d", mode=0o755
    )
    self.install_file(
        self.files_path / "00-setup-kernels.sh", "usr/lib/kernel.d", mode=0o755
    )
    self.install_file(
        self.files_path / "05-prune-kernels.sh", "usr/lib/kernel.d", mode=0o755
    )


@subpackage("base-kernel-devel")
def _(self):
    self.depends = [
        "elftoolchain-devel",
        "flex",
        "gmake",
        "gsed",
        "kmod",
        "libressl-devel",
        "linux-headers",
        "perl",
        "python",
        "xz",
        "zstd-progs",
    ]
    return ["usr/bin/chimera-buildkernel", "usr/bin/chimera-stripko"]
