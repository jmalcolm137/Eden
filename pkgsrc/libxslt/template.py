pkgname = "libxslt"
pkgver = "1.1.45"
pkgrel = 1
build_style = "gnu_configure"
configure_args = [
    "--disable-static",
    "--without-crypto",
    "--without-python",
]
configure_gen = []
hostmakedepends = ["pkgconf"]
makedepends = ["libxml2-devel"]
pkgdesc = "XSLT library"
license = "MIT"
url = "https://xmlsoft.org/XSLT"
source = "https://download.gnome.org/sources/libxslt/1.1/libxslt-1.1.45.tar.xz"
sha256 = "9acfe68419c4d06a45c550321b3212762d92f41465062ca4ea19e632ee5d216e"
# tests need the upstream test suite corpus
options = ["!check", "!distlicense"]


@subpackage("libxslt-devel")
def _(self):
    return self.default_devel()


@subpackage("libxslt-progs")
def _(self):
    return self.default_progs()

