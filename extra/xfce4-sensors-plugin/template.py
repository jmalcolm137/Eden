pkgname = "xfce4-sensors-plugin"
pkgver = "1.5.0"
pkgrel = 0
build_style = "meson"
configure_args = [
    # FIXME: lm-sensors is not ported yet
    "-Dlibsensors=disabled",
    "-Dxnvctrl=disabled",
    "-Dprocacpi=disabled",
    "-Dsysfsacpi=enabled",
]
hostmakedepends = [
    "gettext",
    "glib-devel",
    "muon",
    "pkgconf",
    "samurai",
]
makedepends = [
    "gtk+3-devel",
    "libnotify-devel",
    "libxfce4ui-devel",
    "libxfce4util-devel",
    "xfce4-panel-devel",
]
pkgdesc = "Xfce hardware sensors panel plugin"
license = "GPL-2.0-or-later"
url = "https://docs.xfce.org/panel-plugins/xfce4-sensors-plugin/start"
source = "https://archive.xfce.org/src/panel-plugins/xfce4-sensors-plugin/1.5/xfce4-sensors-plugin-1.5.0.tar.xz"
sha256 = "840442b87fdddcd8595bd9f83ea8b81f771fe296bb9d2abf0e1979e208727ae9"
# upstream tests need a display and a running session bus
options = ["!check"]
