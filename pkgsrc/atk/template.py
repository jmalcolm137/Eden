pkgname = "atk"
pkgver = "2.38.0"
pkgrel = 0
build_style = "meson"
configure_args = [
    "-Ddocs=false",
    "-Dintrospection=false",
]
hostmakedepends = [
    "glib-devel",
    "muon",
    "pkgconf",
    "samurai",
]
makedepends = [
    "glib-devel",
]
pkgdesc = "Accessibility toolkit"
license = "LGPL-2.1-or-later"
url = "https://gitlab.gnome.org/GNOME/atk"
source = "https://download.gnome.org/sources/atk/2.38/atk-2.38.0.tar.xz"
sha256 = "ac4de2a4ef4bd5665052952fe169657e65e895c5057dffb3c2a810f6191a0c36"
# tests require a display or a full graphics stack
options = ["!check"]


@subpackage("atk-devel")
def _(self):
    return self.default_devel()


def post_install(self):
    self.install_license("COPYING")
