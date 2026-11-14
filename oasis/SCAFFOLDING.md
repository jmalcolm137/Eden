# Scaffolded Oasis packages

No packages remain scaffolded-only: every Oasis `pkg/` entry now has a
`template.py` in this repository.

12 templates are intentionally marked broken because their
build dependencies or source acquisition are not yet available:

| Package | Blocker |
| --- | --- |
| `acme-client` | blocked on the Oasis openbsd source/header package |
| `b3sum` | requires a Rust toolchain not yet available in core |
| `catgirl` | upstream git host is not reachable over TLS and the source is not vendored |
| `fspec-sync` | requires b3sum/Rust and the Oasis recovery toolchain |
| `libfido2` | requires the Oasis openbsd libbsd/header package |
| `mpv` | requires a full libplacebo build not yet available in the tree |
| `openbsd` | large OpenBSD source package not yet ported |
| `pounce` | upstream git host is not reachable over TLS and the source is not vendored |
| `sshfs` | requires glib/gthread, which are not part of the current tree |
| `syslinux` | complex BIOS/EFI bootloader build not yet ported |
| `u-boot` | cross-target bootloader build not yet ported |
| `zfs` | kernel/userland ZFS build not yet ported |
