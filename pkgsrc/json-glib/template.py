pkgname = "json-glib"
pkgver = "1.10.8"
pkgrel = 0
archs = ["x86_64"]
build_style = "meson"
configure_args = [
    "-Ddocumentation=disabled",
    "-Dinstalled_tests=false",
    "-Dintrospection=disabled",
    "-Dman=false",
    "-Dtests=false",
]
hostmakedepends = ["meson-real", "pkgconf", "samurai"]
makedepends = ["glib-devel"]
pkgdesc = "JSON library for GLib"
license = "LGPL-2.1-or-later"
url = "https://gitlab.gnome.org/GNOME/json-glib"
source = f"https://download.gnome.org/sources/json-glib/1.10/json-glib-{pkgver}.tar.xz"
sha256 = "55c5c141a564245b8f8fbe7698663c87a45a7333c2a2c56f06f811ab73b212dd"
# the test suite needs a full GLib test harness
options = ["!check"]


@subpackage("json-glib-devel")
def _(self):
    return self.default_devel()


def post_install(self):
    self.install_license("COPYING")
