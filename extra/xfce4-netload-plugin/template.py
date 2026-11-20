pkgname = "xfce4-netload-plugin"
pkgver = "1.5.0"
pkgrel = 0
build_style = "meson"
configure_args = [
    "-Dtests=false",
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
    "libxfce4ui-devel",
    "xfce4-panel-devel",
]
pkgdesc = "Xfce network load panel plugin"
license = "GPL-2.0-or-later"
url = "https://docs.xfce.org/panel-plugins/xfce4-netload-plugin/start"
source = "https://archive.xfce.org/src/panel-plugins/xfce4-netload-plugin/1.5/xfce4-netload-plugin-1.5.0.tar.xz"
sha256 = "a868be8f73e8396c2d61903d46646993c5130d16ded71ddb5da9088abf7cb7ba"
# upstream tests need a display and a running session bus
options = ["!check"]
