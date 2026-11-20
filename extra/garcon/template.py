pkgname = "garcon"
pkgver = "4.21.0"
pkgrel = 0
build_style = "meson"
configure_args = [
    "-Dintrospection=false",
    "-Dgtk-doc=false",
    "-Dtests=false",
]
hostmakedepends = [
    "gettext",
    "glib-devel",
    "muon",
    "pkgconf",
    "samurai",
    "xfce4-dev-tools",
]
makedepends = [
    "glib-devel",
    "gtk+3-devel",
    "libxfce4ui-devel",
    "libxfce4util-devel",
]
pkgdesc = "Xfce implementation of the freedesktop compliant menu spec"
license = "LGPL-2.0-or-later"
url = "https://docs.xfce.org/xfce/garcon/start"
source = "https://archive.xfce.org/src/xfce/garcon/4.21/garcon-4.21.0.tar.xz"
sha256 = "3acc3f6b81059199f4e6646da7b6ca39edf84ea90dd3ff87088ffca6aa108269"
# upstream tests need a display and a running session bus
options = ["!check", "etcfiles"]


@subpackage("garcon-devel")
def _(self):
    return self.default_devel()
