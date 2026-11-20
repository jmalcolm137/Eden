pkgname = "xfce4-diskperf-plugin"
pkgver = "2.8.0"
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
]
pkgdesc = "Xfce disk performance panel plugin"
license = "BSD-2-Clause"
url = "https://docs.xfce.org/panel-plugins/xfce4-diskperf-plugin/start"
source = "https://archive.xfce.org/src/panel-plugins/xfce4-diskperf-plugin/2.8/xfce4-diskperf-plugin-2.8.0.tar.xz"
sha256 = "3833920a3a4a81b3c676c4fab6dd178f4a222d66f316a0783a9149a0153b7fb6"
# upstream tests need a display and a running session bus
options = ["!check"]


def post_install(self):
    self.install_license("COPYING")
