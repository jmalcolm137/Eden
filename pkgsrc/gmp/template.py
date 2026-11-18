pkgname = "gmp"
pkgver = "6.3.0"
pkgrel = 1
build_style = "gnu_configure"
configure_args = ["--enable-cxx"]
configure_gen = []
hostmakedepends = ["m4"]
pkgdesc = "GNU multiple precision arithmetic library"
license = "LGPL-3.0-or-later OR GPL-2.0-or-later"
url = "https://gmplib.org"
source = f"https://gmplib.org/download/gmp/gmp-{pkgver}.tar.bz2"
sha256 = "ac28211a7cfb609bae2e2c8d6058d66c8fe96434f740cf6fe2e47b000d1c20cb"
# tests are extremely slow
options = ["!check"]


@subpackage("gmp-devel")
def _(self):
    return self.default_devel()


@subpackage("gmp-cxx")
def _(self):
    self.subdesc = "C++ bindings"
    return ["usr/lib/libgmpxx.so.*"]


def post_install(self):
    self.install_license("COPYINGv3")
