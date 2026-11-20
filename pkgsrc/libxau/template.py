pkgname = "libxau"
pkgver = "1.0.12"
pkgrel = 0
build_style = "gnu_configure"
configure_env = {"M4": "/usr/bin/gm4"}
hostmakedepends = ["automake", "libtool", "pkgconf", "xorg-util-macros"]
makedepends = ["xorgproto"]
pkgdesc = "Authorization Protocol for X"
license = "MIT"
url = "https://xorg.freedesktop.org"
source = f"https://xorg.freedesktop.org/releases/individual/lib/libXau-{pkgver}.tar.gz"
sha256 = "2402dd938da4d0a332349ab3d3586606175e19cb32cb9fe013c19f1dc922dcee"
# upstream test suites need a full X session
options = ["!check"]


def post_install(self):
    self.install_license("COPYING")


@subpackage("libxau-devel")
def _(self):
    return self.default_devel()
