pkgname = "xfce4-weather-plugin"
pkgver = "0.12.0"
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
    "json-c-devel",
    "libsoup3-devel",
    "libxfce4ui-devel",
    "libxfce4util-devel",
    "libxml2-devel",
    "upower-devel",
    "xfce4-panel-devel",
    "xfconf-devel",
]
pkgdesc = "Xfce weather panel plugin"
license = "GPL-2.0-or-later"
url = "https://docs.xfce.org/panel-plugins/xfce4-weather-plugin/start"
source = f"https://archive.xfce.org/src/panel-plugins/xfce4-weather-plugin/0.12/xfce4-weather-plugin-0.12.0.tar.xz"
sha256 = "5dd90b032c06ef4b64b818023154ef9463a2c694a0290e57f3412296c7545ff6"
# upstream tests need a display and a running session bus
options = ["!check"]


def pre_build(self):
    # muon passes the build directory as the gresource source directory
    self.cp(
        "panel-plugin/weather-config.ui",
        "build/panel-plugin/weather-config.ui",
    )
