pkgname = "opus"
pkgver = "1.5.2"
pkgrel = 1
build_style = "gnu_configure"
configure_args = [
    "--disable-doc",
    "--disable-extra-programs",
    "--disable-shared",
    "--enable-static",
]
configure_gen = []
pkgdesc = "Interactive speech and audio codec"
license = "BSD-3-Clause"
url = "https://opus-codec.org"
source = f"https://github.com/xiph/opus/releases/download/v{pkgver}/opus-{pkgver}.tar.gz"
sha256 = "65c1d2f78b9f2fb20082c38cbe47c951ad5839345876e46941612ee87f9a7ce1"
# no test suite in the Oasis recipe
options = ["!check"]


@subpackage("opus-devel")
def _(self):
    return ["usr/include", "usr/lib/pkgconfig"]


@subpackage("opus-devel-static")
def _(self):
    return ["usr/lib/*.a"]


def post_install(self):
    self.install_license("COPYING")
