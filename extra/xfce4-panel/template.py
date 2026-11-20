pkgname = "xfce4-panel"
pkgver = "4.21.3"
pkgrel = 3
build_style = "meson"
configure_args = [
    "-Dx11=disabled",
    "-Dwayland=enabled",
    "-Dintrospection=false",
    "-Dvala=disabled",
    "-Dgtk-doc=false",
    "-Dgtk-layer-shell=enabled",
    "-Ddbusmenu=disabled",
]
hostmakedepends = [
    "gettext",
    "glib-devel",
    "muon",
    "pkgconf",
    "samurai",
    "wayland-progs",
    "xfce4-dev-tools",
]
makedepends = [
    "cairo-devel",
    "exo-devel",
    "garcon-devel",
    "glib-devel",
    "gtk+3-devel",
    "gtk-layer-shell-devel",
    "libxfce4ui-devel",
    "libxfce4util-devel",
    "libxfce4windowing-devel",
    "libyaml-devel",
    "wayland-devel",
    "wayland-protocols",
    "xfce4-session-devel",
    "xfconf-devel",
]
pkgdesc = "Xfce panel"
license = "GPL-2.0-or-later AND LGPL-2.1-or-later"
url = "https://docs.xfce.org/xfce/xfce4-panel/start"
source = "https://archive.xfce.org/src/xfce/xfce4-panel/4.21/xfce4-panel-4.21.3.tar.xz"
sha256 = "daa277162735e024552586dac0df24bf9e0ed3fdcaa3bc4210b97c0679013db3"
# upstream tests need a display and a running session bus
options = ["!check", "etcfiles"]


@subpackage("xfce4-panel-devel")
def _(self):
    return self.default_devel()
