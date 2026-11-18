pkgname = "ristretto"
pkgver = "0.14.0"
pkgrel = 0
build_style = "meson"
configure_args = [
    "-Dlibx11=disabled",
]
hostmakedepends = [
    "gettext",
    "glib-devel",
    "muon",
    "pkgconf",
    "samurai",
]
makedepends = [
    "cairo-devel",
    "exo-devel",
    "file-devel",
    "glib-devel",
    "gtk+3-devel",
    "libexif-devel",
    "libxfce4ui-devel",
    "libxfce4util-devel",
    "xfconf-devel",
]
pkgdesc = "Xfce image viewer"
license = "GPL-2.0-or-later"
url = "https://docs.xfce.org/apps/ristretto/start"
source = f"https://archive.xfce.org/src/apps/ristretto/0.14/ristretto-0.14.0.tar.xz"
sha256 = "502cf1577de14b38132dc89e56884c5e10f86f6a028d8dde379a8839110fda55"
# upstream tests need a display and a running session bus
options = ["!check"]


def pre_build(self):
    # muon passes the build directory as the gresource source directory
    self.cp("src/main_window_ui.xml", "build/src/main_window_ui.xml")
