pkgname = "xfce4-mount-plugin"
pkgver = "1.2.0"
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
    "glib-devel",
    "gtk+3-devel",
    "libxfce4ui-devel",
    "libxfce4util-devel",
    "xfce4-panel-devel",
]
pkgdesc = "Mount plugin for the Xfce panel"
license = "GPL-2.0-or-later"
url = "https://docs.xfce.org/xfce/xfce4-mount-plugin/start"
source = f"https://archive.xfce.org/src/panel-plugins/xfce4-mount-plugin/1.2/xfce4-mount-plugin-1.2.0.tar.xz"
sha256 = "adef71a83078e7dc45997e57411f8c43080a0204159a8b8db2ade0a9877e7b4c"
# upstream tests need a display and a running session bus
options = ["!check"]
