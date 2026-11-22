pkgname = "patchelf"
pkgver = "0.18.0"
pkgrel = 0
build_style = "gnu_configure"
# release tarball ships a generated configure script
configure_gen = []
pkgdesc = "Utility for modifying existing ELF executables and libraries"
license = "GPL-3.0-or-later"
url = "https://github.com/NixOS/patchelf"
source = f"https://github.com/NixOS/patchelf/releases/download/{pkgver}/patchelf-{pkgver}.tar.bz2"
sha256 = "1952b2a782ba576279c211ee942e341748fdb44997f704dd53def46cd055470b"
# upstream tests build a large matrix and need a full toolchain
options = ["!check"]
