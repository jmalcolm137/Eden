pkgname = "libexif"
pkgver = "0.6.26"
pkgrel = 1
build_style = "gnu_configure"
configure_args = [
    "--disable-docs",
    "--disable-static",
]
configure_gen = []
hostmakedepends = ["pkgconf"]
pkgdesc = "EXIF data manipulation library"
license = "LGPL-2.1-or-later"
url = "https://libexif.github.io"
source = f"https://github.com/libexif/libexif/releases/download/v{pkgver}/libexif-{pkgver}.tar.bz2"
sha256 = "0830ed253fceeb60444fb309598bc8a9491d3007dc054aad3a50a347c5597c57"
# tests need the upstream test corpus
options = ["!check"]


@subpackage("libexif-devel")
def _(self):
    return self.default_devel()


def post_install(self):
    self.install_license("COPYING")
