pkgname = "libpsl"
pkgver = "0.23.3"
pkgrel = 1
build_style = "meson"
configure_args = [
    "-Dbuiltin=true",
    "-Ddocs=false",
    "-Druntime=no",
    "-Dtests=false",
]
hostmakedepends = ["meson-real", "pkgconf", "python", "samurai"]
pkgdesc = "Public Suffix List library"
license = "MIT"
url = "https://github.com/rockdaboot/libpsl"
source = f"https://github.com/rockdaboot/libpsl/releases/download/{pkgver}/libpsl-{pkgver}.tar.gz"
sha256 = "93941f85a1e7bd593fa94f299233cb5dfc91cd144fd9a78a6ceb75001c5b03be"
# tests need the upstream test data
options = ["!check"]


@subpackage("libpsl-devel")
def _(self):
    return self.default_devel()


def post_install(self):
    self.install_license("COPYING")
