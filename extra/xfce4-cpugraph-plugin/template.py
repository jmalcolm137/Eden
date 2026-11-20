pkgname = "xfce4-cpugraph-plugin"
pkgver = "1.3.0"
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
    "libxfce4util-devel",
    "xfce4-panel-devel",
    "xfconf-devel",
]
pkgdesc = "Xfce clipboard manager app and panel plugin"
license = "GPL-2.0-or-later"
url = "https://docs.xfce.org/panel-plugins/xfce4-cpugraph-plugin/start"
source = "https://archive.xfce.org/src/panel-plugins/xfce4-cpugraph-plugin/1.3/xfce4-cpugraph-plugin-1.3.0.tar.xz"
sha256 = "c3305edea13ae785ea8b7ce8efbb40b5d5cac69a6f8bf790e4f2efaa780ca097"
# upstream tests need a display and a running session bus
options = ["!check"]
