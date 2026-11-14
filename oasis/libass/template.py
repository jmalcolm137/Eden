pkgname = "libass"
pkgver = "0.14.0"
pkgrel = 1
# Oasis pkg/libass/src
_commit = "73284b676b12b47e17af2ef1b430527299e10c17"
build_style = "gnu_configure"
configure_args = ["--disable-fontconfig", "--disable-require-system-font-provider"]
configure_gen = []
makedepends = ["freetype", "fribidi-devel"]
pkgdesc = "Subtitle rendering library"
license = "ISC"
url = "https://github.com/libass/libass"
source = f"{url}/releases/download/{pkgver}/libass-{pkgver}.tar.xz"
sha256 = "881f2382af48aead75b7a0e02e65d88c5ebd369fe46bc77d9270a94aa8fd38a2"
# no test suite in the Oasis recipe
options = ["!check"]


@subpackage("libass-devel")
def _(self):
    return self.default_devel()


def post_install(self):
    self.install_license("COPYING")
