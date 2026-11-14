pkgname = "fribidi"
pkgver = "1.0.11"
pkgrel = 0
build_style = "gnu_configure"
configure_gen = []
pkgdesc = "Bidirectional text library"
license = "LGPL-2.1-or-later"
url = "https://github.com/fribidi/fribidi"
source = f"{url}/releases/download/v{pkgver}/fribidi-{pkgver}.tar.xz"
sha256 = "30f93e9c63ee627d1a2cedcf59ac34d45bf30240982f99e44c6e015466b4e73d"
# no test suite in the Oasis recipe
options = ["!check"]


@subpackage("fribidi-devel")
def _(self):
    return self.default_devel()
