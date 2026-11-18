pkgname = "libogg"
pkgver = "1.3.6"
pkgrel = 1
build_style = "gnu_configure"
configure_args = ["--disable-static"]
configure_gen = []
hostmakedepends = ["pkgconf"]
pkgdesc = "Ogg bitstream library"
license = "BSD-3-Clause"
url = "https://www.xiph.org/ogg"
source = "https://downloads.xiph.org/releases/ogg/libogg-1.3.6.tar.xz"
sha256 = "5c8253428e181840cd20d41f3ca16557a9cc04bad4a3d04cce84808677fa1061"
# no test suite needed
options = ["!check"]


@subpackage("libogg-devel")
def _(self):
    return self.default_devel()


def post_install(self):
    self.install_license("COPYING")
