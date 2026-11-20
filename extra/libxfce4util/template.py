pkgname = "libxfce4util"
pkgver = "4.21.0"
pkgrel = 1
build_style = "meson"
configure_args = [
    "-Dintrospection=false",
    "-Dvala=disabled",
    "-Dgtk-doc=false",
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
]
pkgdesc = "Utility library for Xfce"
license = "LGPL-2.0-or-later"
url = "https://docs.xfce.org/xfce/libxfce4util/start"
source = "https://archive.xfce.org/src/xfce/libxfce4util/4.21/libxfce4util-4.21.0.tar.xz"
sha256 = "205677cb96b778e5079eeac80f3a636d2a909b08fcf2aa05bfe4513c69c27f29"
# upstream tests need a display and a running session bus
options = ["!check"]


@subpackage("libxfce4util-devel")
def _(self):
    return self.default_devel()
