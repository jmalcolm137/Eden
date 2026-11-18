pkgname = "xfce4-docklike-plugin"
pkgver = "0.5.1"
pkgrel = 0
build_style = "meson"
configure_args = [
    "-Dx11=disabled",
    "-Dwayland=enabled",
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
    "cairo-devel",
    "gtk+3-devel",
    "gtk-layer-shell-devel",
    "libxfce4ui-devel",
    "libxfce4util-devel",
    "libxfce4windowing-devel",
    "xfce4-panel-devel",
]
pkgdesc = "Xfce taskbar panel plugin"
license = "GPL-3.0-or-later"
url = "https://docs.xfce.org/panel-plugins/xfce4-docklike-plugin/start"
source = f"https://archive.xfce.org/src/panel-plugins/xfce4-docklike-plugin/0.5/xfce4-docklike-plugin-0.5.1.tar.xz"
sha256 = "9d7b355c2be37fb0a73b77b4ed75f092d23c012a67b102c9f847c55ddc3095df"
# upstream tests need a display and a running session bus
options = ["!check"]


def pre_build(self):
    # muon passes the build directory as the gresource source directory
    self.cp("src/_dialogs.ui", "build/src/_dialogs.ui")
