pkgname = "xfce4-panel-profiles"
pkgver = "1.1.1"
pkgrel = 0
build_style = "meson"
configure_args = [
    "-Dcheck-runtime-dependencies=false",
]
hostmakedepends = [
    "gettext",
    "glib-devel",
    "muon",
    "pkgconf",
    "python",
    "samurai",
]
depends = [
    "gtk+3",
    "python",
    "python-gobject",
    "xfce4-panel",
]
pkgdesc = "Xfce panel configuration profiles tool"
license = "GPL-2.0-or-later"
url = "https://docs.xfce.org/xfce/xfce4-panel-profiles/start"
source = "https://archive.xfce.org/src/apps/xfce4-panel-profiles/1.1/xfce4-panel-profiles-1.1.1.tar.xz"
sha256 = "0126373a03778bb4894afa151de28d36bfc563ddab96d3bd7c63962350d34ba2"
# upstream tests need a display and a running session bus
options = ["!check"]
