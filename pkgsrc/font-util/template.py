pkgname = "font-util"
pkgver = "1.4.1"
pkgrel = 0
build_style = "gnu_configure"
configure_args = ["--with-fontrootdir=${datadir}/fonts"]
hostmakedepends = ["automake", "pkgconf", "xorg-util-macros"]
pkgdesc = "X.org font utilities"
license = "MIT"
url = "https://xorg.freedesktop.org"
source = f"https://xorg.freedesktop.org/releases/individual/font/font-util-{pkgver}.tar.gz"
sha256 = "f029ae80cdd75d89bee7f7af61c21e07982adfb9f72344a158b99f91f77ef5ed"


def post_install(self):
    self.install_license("COPYING")


@subpackage("font-util-devel")
def _(self):
    return self.default_devel()
