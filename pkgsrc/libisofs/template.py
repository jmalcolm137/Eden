pkgname = "libisofs"
pkgver = "1.5.6"
pkgrel = 1
build_style = "gnu_configure"
configure_args = ["--disable-static"]
configure_gen = []
hostmakedepends = ["pkgconf"]
makedepends = ["zlib-static"]
pkgdesc = "Library for creating ISO-9660 filesystems"
license = "GPL-2.0-or-later"
url = "https://dev.lovelyhq.com/libburnia"
source = f"https://files.libburnia-project.org/releases/libisofs-{pkgver}.tar.gz"
sha256 = "0152d66a9d340b659fe9c880eb9190f3570fb477ac07cf52e8bcd134a1d30d70"
# tests need the full upstream tree
options = ["!check"]


@subpackage("libisofs-devel")
def _(self):
    return self.default_devel()


def post_install(self):
    self.install_license("COPYING")
