pkgname = "xfce4-notes-plugin"
pkgver = "1.12.0"
pkgrel = 0
build_style = "meson"
meson_impl = "meson"
hostmakedepends = [
    "gettext",
    "glib-devel",
    "meson-real",
    "pkgconf",
    "samurai",
    "vala",
]
makedepends = [
    "gtk+3-devel",
    "gtksourceview4-devel",
    "libxfce4ui-devel",
    "libxfce4util-devel",
    "xfce4-panel-devel",
    "xfconf-devel",
]
pkgdesc = "Xfce notes panel plugin"
license = "GPL-2.0-or-later"
url = "https://docs.xfce.org/panel-plugins/xfce4-notes-plugin/start"
source = f"https://archive.xfce.org/src/panel-plugins/xfce4-notes-plugin/1.12/xfce4-notes-plugin-1.12.0.tar.xz"
sha256 = "cf4cc8f2e9785b7032aef6a74f316b8d7945457982295f8465a872b75da46a2a"
# upstream tests need a display and a running session bus
options = ["!check"]

