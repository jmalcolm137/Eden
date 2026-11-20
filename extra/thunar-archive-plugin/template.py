pkgname = "thunar-archive-plugin"
pkgver = "0.6.0"
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
    "libxfce4util-devel",
    "thunar-devel",
]
pkgdesc = "Archive manager integration for Thunar"
license = "GPL-2.0-or-later"
url = "https://docs.xfce.org/xfce/thunar/thunar-archive-plugin"
source = "https://archive.xfce.org/src/thunar-plugins/thunar-archive-plugin/0.6/thunar-archive-plugin-0.6.0.tar.xz"
sha256 = "692708cd047c7a552f2f85fe2ee32f19c7d5be5bf695d0288e8cadf50289db06"
# upstream tests need a display and a running session bus
options = ["!check"]
