pkgname = "libepoxy"
pkgver = "1.5.10"
pkgrel = 1
build_style = "meson"
configure_args = [
    "-Ddocs=false",
    "-Degl=yes",
    "-Dglx=no",
    "-Dtests=false",
    "-Dx11=false",
]
hostmakedepends = [
    "muon",
    "pkgconf",
    "python",
    "samurai",
]
makedepends = [
    "libglvnd-devel",
]
pkgdesc = "Library for handling OpenGL function pointers"
license = "MIT"
url = "https://github.com/anholt/libepoxy"
source = "https://github.com/anholt/libepoxy/archive/1.5.10.tar.gz"
sha256 = "a7ced37f4102b745ac86d6a70a9da399cc139ff168ba6b8002b4d8d43c900c15"
# tests require a display or a full graphics stack
options = ["!check"]


def post_install(self):
    self.install_license("COPYING")


@subpackage("libepoxy-devel")
def _(self):
    return self.default_devel()
