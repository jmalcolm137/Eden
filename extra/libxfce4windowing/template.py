pkgname = "libxfce4windowing"
pkgver = "4.20.7"
pkgrel = 0
build_style = "meson"
configure_args = [
    "-Dx11=disabled",
    "-Dwayland=enabled",
    "-Dintrospection=false",
    "-Dvala=disabled",
    "-Dgtk-doc=false",
    "-Dtests=false",
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
    "gtk+3-devel",
    "libdisplay-info-devel",
    "wayland-devel",
    "wayland-protocols",
]
pkgdesc = "Xfce windowing abstraction library"
license = "LGPL-2.1-or-later"
url = "https://docs.xfce.org/xfce/libxfce4windowing/start"
source = "https://archive.xfce.org/src/xfce/libxfce4windowing/4.20/libxfce4windowing-4.20.7.tar.bz2"
sha256 = "01320b279648ab5b13263f8d260bc5958be599e1eaac77c4503598dfcf96c8bb"
# upstream tests need a display and a running session bus
options = ["!check"]


@subpackage("libxfce4windowing-devel")
def _(self):
    return self.default_devel()
