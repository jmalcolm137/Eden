pkgname = "gtksourceview4"
pkgver = "4.8.4"
pkgrel = 0
build_style = "meson"
configure_args = [
    "-Dgir=false",
    "-Dvapi=false",
]
meson_impl = "meson"
hostmakedepends = [
    "gettext",
    "meson-real",
    "pkgconf",
    "samurai",
]
makedepends = [
    "glib-devel",
    "gtk+3-devel",
    "libxml2-devel",
]
pkgdesc = "Text widget for source code editing"
license = "LGPL-2.1-or-later"
url = "https://wiki.gnome.org/Projects/GtkSourceView"
source = f"https://download.gnome.org/sources/gtksourceview/4.8/gtksourceview-{pkgver}.tar.xz"
sha256 = "7ec9d18fb283d1f84a3a3eff3b7a72b09a10c9c006597b3fbabbb5958420a87d"
# tests need a display
options = ["!check"]


@subpackage("gtksourceview4-devel")
def _(self):
    return self.default_devel()


def post_install(self):
    self.install_license("COPYING")
