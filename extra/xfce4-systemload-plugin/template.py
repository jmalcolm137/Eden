pkgname = "xfce4-systemload-plugin"
pkgver = "1.4.0"
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
    "libgtop-devel",
    "libxfce4ui-devel",
    "libxfce4util-devel",
    "upower-devel",
    "xfce4-panel-devel",
    "xfconf-devel",
]
pkgdesc = "Xfce system load panel plugin"
license = "GPL-2.0-or-later AND BSD-2-Clause"
url = "https://docs.xfce.org/panel-plugins/xfce4-systemload-plugin/start"
source = "https://archive.xfce.org/src/panel-plugins/xfce4-systemload-plugin/1.4/xfce4-systemload-plugin-1.4.0.tar.xz"
sha256 = "6e363bcf845bb88329b52858d65a1ec6e00db5121ae9246e46eb03135d9569c6"
# upstream tests need a display and a running session bus
options = ["!check"]


def post_install(self):
    self.install_license("COPYING")
