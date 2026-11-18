pkgname = "xfce4-time-out-plugin"
pkgver = "1.2.0"
pkgrel = 0
build_style = "meson"
configure_args = [
    "-Dx11=disabled",
]
hostmakedepends = [
    "gettext",
    "glib-devel",
    "muon",
    "pkgconf",
    "samurai",
    "wayland-progs",
]
makedepends = [
    "gtk+3-devel",
    "libxfce4ui-devel",
    "xfce4-panel-devel",
]
pkgdesc = "Xfce time-out panel plugin"
license = "GPL-2.0-or-later"
url = "https://docs.xfce.org/panel-plugins/xfce4-time-out-plugin/start"
source = f"https://archive.xfce.org/src/panel-plugins/xfce4-time-out-plugin/1.2/xfce4-time-out-plugin-1.2.0.tar.xz"
sha256 = "e344d9f82a8acd23d44e7cf9b2efe9599ffff856d9ba1a9be0e67b022c0d2eb2"
# upstream tests need a display and a running session bus
options = ["!check"]
