pkgname = "xfce4-terminal"
pkgver = "1.2.0"
pkgrel = 0
build_style = "meson"
configure_args = [
    "-Dx11=disabled",
    "-Dwayland=enabled",
    "-Dgtk-layer-shell=enabled",
    "-Dlibutempter=disabled",
    "-Ddoc=false",
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
    "exo-devel",
    "glib-devel",
    "gtk-layer-shell-devel",
    "libxfce4ui-devel",
    "vte-gtk3-devel",
    "wayland-devel",
    "wayland-protocols",
]
pkgdesc = "Xfce terminal emulator"
license = "GPL-2.0-or-later"
url = "https://docs.xfce.org/apps/xfce4-terminal/start"
source = "https://archive.xfce.org/src/apps/xfce4-terminal/1.2/xfce4-terminal-1.2.0.tar.xz"
sha256 = "6874c7b975cc3dc3bd636d57ffec723de7458202defe65377593d3a7e0734b94"
# upstream tests need a display and a running session bus
options = ["!check"]
