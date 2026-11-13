pkgname = "file"
pkgver = "5.45"
pkgrel = 0
build_style = "gnu_configure"
configure_args = [
    "--disable-bzlib",
    "--disable-xzlib",
    "--disable-lzlib",
]
configure_gen = []
makedepends = ["zlib-ng-compat-devel"]
pkgdesc = "File type identification utility"
license = "BSD-2-Clause"
url = "https://www.darwinsys.com/file"
source = f"https://astron.com/pub/file/file-{pkgver}.tar.gz"
sha256 = "fc97f51029bb0e2c9f4e3bffefdaf678f0e039ee872b9de5c002a6d09c784d82"
# no test suite in the Oasis recipe
options = ["!check"]


@subpackage("file-devel")
def _(self):
    return self.default_devel()


def post_install(self):
    self.install_license("COPYING")
