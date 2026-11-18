pkgname = "libtasn1"
pkgver = "4.21.0"
pkgrel = 1
build_style = "gnu_configure"
configure_args = ["--disable-static"]
configure_gen = []
hostmakedepends = ["pkgconf"]
pkgdesc = "ASN.1 structure management library"
license = "LGPL-2.1-or-later"
url = "https://www.gnu.org/software/libtasn1"
source = f"https://ftp.gnu.org/gnu/libtasn1/libtasn1-{pkgver}.tar.gz"
sha256 = "1d8a444a223cc5464240777346e125de51d8e6abf0b8bac742ac84609167dc87"
# tests are part of the upstream tree
options = ["!check"]


@subpackage("libtasn1-devel")
def _(self):
    return self.default_devel()


@subpackage("libtasn1-progs")
def _(self):
    return self.default_progs()


def post_install(self):
    self.install_license("COPYING")
