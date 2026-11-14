pkgname = "dav1d"
pkgver = "0.9.2"
pkgrel = 0
build_style = "meson"
configure_args = [
    "-Denable_tools=false",
    "-Denable_tests=false",
    "-Denable_examples=false",
    "-Denable_asm=false",
]
makedepends = ["nasm"]
pkgdesc = "AV1 decoder"
license = "BSD-2-Clause"
url = "https://code.videolan.org/videolan/dav1d"
source = f"https://github.com/videolan/dav1d/archive/refs/tags/{pkgver}.tar.gz"
sha256 = "59a5fc9cc5d8ea780ad71ede6d589ed33fb5179d87780dcf80a00ee854952935"
# no test suite in the Oasis recipe
options = ["!check"]


@subpackage("dav1d-devel")
def _(self):
    return self.default_devel()


def post_install(self):
    self.install_license("COPYING")
