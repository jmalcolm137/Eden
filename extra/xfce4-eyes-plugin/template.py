pkgname = "xfce4-eyes-plugin"
pkgver = "4.7.0"
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
    "gtk+3-devel",
    "libxfce4ui-devel",
    "xfce4-panel-devel",
]
pkgdesc = "Xfce eyes panel plugin"
license = "GPL-2.0-or-later"
url = "https://docs.xfce.org/panel-plugins/xfce4-eyes-plugin/start"
source = "https://archive.xfce.org/src/panel-plugins/xfce4-eyes-plugin/4.7/xfce4-eyes-plugin-4.7.0.tar.xz"
sha256 = "87f9b978ca75abb3aa5edb1315eb65ef98654a662c14621847ddffe8aa6574ad"
# upstream tests need a display and a running session bus
options = ["!check"]
