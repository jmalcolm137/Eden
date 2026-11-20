pkgname = "libndp"
pkgver = "1.9"
pkgrel = 1
build_style = "gnu_configure"
configure_env = {"M4": "/usr/bin/gm4"}
hostmakedepends = ["autoconf", "automake", "gm4", "libtool", "pkgconf"]
pkgdesc = "Library for Neighbor Discovery Protocol"
license = "LGPL-2.1-or-later"
url = "http://libndp.org"
source = f"https://github.com/jpirko/libndp/archive/refs/tags/v{pkgver}.tar.gz"
sha256 = "e564f5914a6b1b799c3afa64c258824a801c1b79a29e2fe6525b682249c65261"
# the 1.9 sources predate stricter clang pointer diagnostics
tool_flags = {"CFLAGS": ["-Wno-incompatible-pointer-types"]}
# no test suite
options = ["!check"]


@subpackage("libndp-devel")
def _(self):
    return self.default_devel()


def post_install(self):
    self.install_license("COPYING")
