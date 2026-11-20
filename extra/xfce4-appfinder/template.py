pkgname = "xfce4-appfinder"
pkgver = "4.21.1"
pkgrel = 0
build_style = "meson"
hostmakedepends = [
    "gettext",
    "glib-devel",
    "muon",
    "pkgconf",
    "samurai",
]
makedepends = [
    "garcon-devel",
    "glib-devel",
    "gtk+3-devel",
    "libxfce4ui-devel",
    "libxfce4util-devel",
    "xfconf-devel",
]
pkgdesc = "Xfce application finder"
license = "GPL-2.0-or-later"
url = "https://docs.xfce.org/xfce/xfce4-appfinder/start"
source = "https://archive.xfce.org/src/xfce/xfce4-appfinder/4.21/xfce4-appfinder-4.21.1.tar.xz"
sha256 = "62fba13ec05066e73200f5a34c2fa1e7a1a7c4dbefffbaf29af9e9e97bb4a7c9"
# upstream tests need a display and a running session bus
options = ["!check"]


def pre_build(self):
    # muon passes the build directory as the gresource source directory
    self.cp(
        "src/appfinder-preferences.glade",
        "build/src/appfinder-preferences.glade",
    )
