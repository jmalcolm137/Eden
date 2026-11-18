pkgname = "nghttp2"
pkgver = "1.71.0"
pkgrel = 1
build_style = "gnu_configure"
configure_args = [
    "--disable-examples",
    "--disable-hpack-tools",
    "--disable-static",
    "--enable-lib-only",
]
configure_gen = []
hostmakedepends = ["pkgconf"]
makedepends = ["zlib-static"]
pkgdesc = "HTTP/2 C library"
license = "MIT"
url = "https://nghttp2.org"
source = f"https://github.com/nghttp2/nghttp2/releases/download/v{pkgver}/nghttp2-{pkgver}.tar.xz"
sha256 = "c0f55121d88650e4b9227aec28cebaf664d2417ca60fe70be0f8d38829f52116"
# lib-only build, tests need the full tree
options = ["!check"]


@subpackage("nghttp2-devel")
def _(self):
    return self.default_devel()


def post_install(self):
    self.install_license("COPYING")
