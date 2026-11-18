pkgname = "xfce4-places-plugin"
pkgver = "1.9.0"
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
    "exo-devel",
    "gtk+3-devel",
    "libnotify-devel",
    "libxfce4ui-devel",
    "libxfce4util-devel",
    "xfce4-panel-devel",
    "xfconf-devel",
]
pkgdesc = "Xfce folders and media quick access panel plugin"
license = "GPL-2.0-or-later"
url = "https://docs.xfce.org/panel-plugins/xfce4-places-plugin/start"
source = f"https://archive.xfce.org/src/panel-plugins/xfce4-places-plugin/1.9/xfce4-places-plugin-1.9.0.tar.xz"
sha256 = "76d95687e0bea267465e832eea6266563a18d2219192f9e8af6f88e899262e43"
# upstream tests need a display and a running session bus
options = ["!check"]
