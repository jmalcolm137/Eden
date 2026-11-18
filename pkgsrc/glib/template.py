pkgname = "glib"
pkgver = "2.90.1"
pkgrel = 0
build_style = "meson"
configure_args = [
    "-Ddocumentation=false",
    "-Ddtrace=disabled",
    "-Dinstalled_tests=false",
    "-Dintrospection=disabled",
    "-Dlibelf=disabled",
    "-Dlibmount=disabled",
    "-Dman-pages=disabled",
    "-Dmultiarch=false",
    "-Dnls=disabled",
    "-Dselinux=disabled",
    "-Dsysprof=disabled",
    "-Dsystemtap=disabled",
    "-Dtests=false",
]
hostmakedepends = [
    "gettext",
    "muon",
    "pkgconf",
    "python",
    "samurai",
]
makedepends = [
    "libffi8-devel",
    "pcre2-devel",
    "zlib-static",
]
depends = ["python"]
triggers = ["/usr/lib/gio/modules", "/usr/share/glib-2.0/schemas"]
pkgdesc = "GObject-based C utility library"
license = "LGPL-2.1-or-later"
url = "https://wiki.gnome.org/Projects/GLib"
source = "https://download.gnome.org/sources/glib/2.90/glib-2.90.1.tar.xz"
sha256 = "93c941aa17d5eb1d53fe838365f29a8b4e539c222a256d974ec8f30fc413e396"
# tests require a display or a full graphics stack
options = ["!check"]


@subpackage("glib-devel")
def _(self):
    return self.default_devel()


def post_install(self):
    self.install_license("COPYING")
