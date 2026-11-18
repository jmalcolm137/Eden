pkgname = "xfce4-whiskermenu-plugin"
pkgver = "2.10.1"
pkgrel = 0
build_style = "meson"
configure_args = [
    # FIXME: accountsservice is not ported yet
    "-Daccountsservice=disabled",
    "-Dgtk-layer-shell=enabled",
]
hostmakedepends = [
    "gettext",
    "glib-devel",
    "muon",
    "pkgconf",
    "samurai",
]
makedepends = [
    "exo-devel",
    "garcon-devel",
    "gtk+3-devel",
    "gtk-layer-shell-devel",
    "libxfce4ui-devel",
    "libxfce4util-devel",
    "xfce4-panel-devel",
    "xfconf-devel",
]
pkgdesc = "Xfce application launcher panel plugin"
license = "GPL-2.0-or-later"
url = "https://docs.xfce.org/panel-plugins/xfce4-whiskermenu-plugin/start"
source = f"https://archive.xfce.org/src/panel-plugins/xfce4-whiskermenu-plugin/2.10/xfce4-whiskermenu-plugin-2.10.1.tar.xz"
sha256 = "8b5a777a5d9df1f1c39b109ba8b2d045cb2cc02c41a9a297aa00dcb2a4520530"
# upstream tests need a display and a running session bus
options = ["!check"]
