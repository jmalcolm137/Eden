pkgname = "isl"
pkgver = "0.27"
pkgrel = 0
build_style = "gnu_configure"
configure_gen = []
hostmakedepends = ["pkgconf"]
makedepends = ["gmp-devel"]
pkgdesc = "Integer Set Library"
license = "MIT"
url = "https://libisl.sourceforge.io"
source = (
    f"https://downloads.sourceforge.net/project/libisl/isl-{pkgver}.tar.bz2"
)
sha256 = "626335529331f7c89fec493de929e2e92fb3d8cc860fc7af554e0518ee0029ee"
# no test suite
options = ["!check"]


def post_install(self):
    self.install_license("LICENSE")


@subpackage("isl-devel")
def _(self):
    return self.default_devel()
