pkgname = "xfce4-wavelan-plugin"
pkgver = "0.7.0"
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
    "libxfce4ui-devel",
    "linux-headers",
    "xfce4-panel-devel",
]
pkgdesc = "Xfce WLAN stats panel plugin"
license = "BSD-2-Clause"
url = "https://docs.xfce.org/panel-plugins/xfce4-wavelan-plugin/start"
source = f"https://archive.xfce.org/src/panel-plugins/xfce4-wavelan-plugin/0.7/xfce4-wavelan-plugin-0.7.0.tar.xz"
sha256 = "5fdce1e1b0d29d0a258dca86bab9d4edcbc12098134b92e00ea1502086a49116"
# upstream tests need a display and a running session bus
options = ["!check"]


def post_install(self):
    self.install_license("COPYING")
