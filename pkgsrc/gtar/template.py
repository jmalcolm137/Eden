pkgname = "gtar"
pkgver = "1.35"
pkgrel = 0
build_style = "gnu_configure"
configure_args = ["--program-prefix=g"]
configure_gen = []
hostmakedepends = ["pkgconf"]
pkgdesc = "GNU tape archiver"
license = "GPL-3.0-or-later"
url = "https://www.gnu.org/software/tar"
source = f"https://ftp.gnu.org/gnu/tar/tar-{pkgver}.tar.xz"
sha256 = "4d62ff37342ec7aed748535323930c7cf94acf71c3591882b26a7ea50f3edc16"
# tests need a full userland and remote-tape setup
options = ["!check"]
