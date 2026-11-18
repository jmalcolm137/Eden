pkgname = "xfce4-genmon-plugin"
pkgver = "4.3.0"
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
pkgdesc = "Xfce generic program monitor panel plugin"
license = "LGPL-2.1-or-later"
url = "https://docs.xfce.org/panel-plugins/xfce4-genmon-plugin/start"
source = f"https://archive.xfce.org/src/panel-plugins/xfce4-genmon-plugin/4.3/xfce4-genmon-plugin-4.3.0.tar.xz"
sha256 = "077197911d84e5ba22e7bb895ce6c038dbbd8e8e0067ed6f4e48502b7167a282"
# upstream tests need a display and a running session bus
options = ["!check"]
