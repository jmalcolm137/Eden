# Scaffolded Oasis packages

Metadata copied from the Oasis `pkg/` tree for packages that do not yet
have a buildable cbuild template in `core/` or `oasis/`.

Each directory contains the Oasis recipe metadata (`gen.lua`, `ver`,
`config.h`, patches, helper files) and a `SOURCE.txt` describing where
the upstream source comes from. There is deliberately no `template.py`:
add one only when the package has actually been ported, then list it in
`oasis-packages.txt`.

Scaffolded packages: 14

| Package | Version | Source kind | Source |
| --- | --- | --- | --- |
| `acme-client` | - | source-package | openbsd |
| `b3sum` | 1.5.0 r0 | git-submodule | https://git.sr.ht/~mcf/b3sum |
| `catgirl` | 2.2a | git-submodule | https://git.causal.agency/catgirl |
| `fspec-sync` | a79592936c r0 | git-submodule | https://github.com/oasislinux/fspec-sync.git |
| `libfido2` | 1.9.0 r0 | git-submodule | https://github.com/oasislinux/libfido2.git |
| `mpv` | 0.38.0 r1 | git-submodule | https://github.com/mpv-player/mpv.git |
| `mupdf` | 1.18.0 r1 | git-submodule | https://github.com/oasislinux/mupdf.git |
| `openbsd` | 8.0 | tarball | https://cloudflare.cdn.openbsd.org/pub/OpenBSD/8.0/src.tar.gz |
| `pounce` | 3.0 r0 | git-submodule | https://git.causal.agency/pounce |
| `sshfs` | 3.6.0 r0 | git-submodule | https://github.com/libfuse/sshfs.git |
| `syslinux` | 6.03 r4 | tarball | https://www.kernel.org/pub/linux/utils/boot/syslinux/syslinux-6.03.tar.xz |
| `u-boot` | 2021.04 r3 | tarball | ftp://ftp.denx.de/pub/u-boot/u-boot-2021.04.tar.bz2 |
| `zfs` | 2.4.0 r2 | tarball | https://github.com/openzfs/zfs/releases/download/zfs-2.4.0/zfs-2.4.0.tar.gz |
| `zlib` | 1.3.1 r0 | git-submodule | https://github.com/madler/zlib.git |
