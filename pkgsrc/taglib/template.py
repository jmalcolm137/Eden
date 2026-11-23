pkgname = "taglib"
pkgver = "2.3.2"
pkgrel = 1
build_style = "cmake"
configure_args = [
    "-DBUILD_EXAMPLES=OFF",
    "-DBUILD_SHARED_LIBS=ON",
    "-DBUILD_TESTING=OFF",
]
hostmakedepends = ["cmake", "meson-real", "pkgconf"]
makedepends = ["zlib"]
pkgdesc = "Audio metadata library"
license = "LGPL-2.1-or-later OR MPL-1.1"
url = "https://taglib.org"
source = "https://taglib.github.io/releases/taglib-2.3.2.tar.gz"
sha256 = "3ca2d8afaa7f1cf7f6ed10e511ebc368bfacd6dcaa3dbfa690b89e502e8963dc"
# tests need a large media corpus
options = ["!check"]


@subpackage("taglib-devel")
def _(self):
    return self.default_devel()


def post_install(self):
    self.install_license("COPYING.LGPL")
