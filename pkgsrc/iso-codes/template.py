pkgname = "iso-codes"
pkgver = "4.16.0"
pkgrel = 1
build_style = "gnu_configure"
configure_args = ["--disable-silent-rules"]
configure_gen = []
hostmakedepends = ["pkgconf", "python"]
pkgdesc = "ISO language, territory, currency and script codes"
license = "LGPL-2.1-or-later"
url = "https://salsa.debian.org/iso-codes-team/iso-codes"
source = f"https://salsa.debian.org/iso-codes-team/iso-codes/-/archive/v{pkgver}/iso-codes-v{pkgver}.tar.bz2"
sha256 = "51800494b89686772f0aeb3f803f818d084c236dcfcf3c04cea047a38a6c3240"
# data-only package, tests need the full tree
options = ["!check"]


def post_install(self):
    self.install_license("COPYING")
