pkgname = "gspell"
pkgver = "1.14.5"
pkgrel = 0
build_style = "meson"
configure_args = [
    "-Dgobject_introspection=false",
    "-Dgspell_app=true",
    "-Dtests=false",
    "-Dgtk_doc=false",
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
    "enchant2-devel",
    "glib-devel",
    "gtk+3-devel",
    "icu-devel",
]
pkgdesc = "Spell-checking support for GTK applications"
license = "LGPL-2.1-or-later"
url = "https://gitlab.gnome.org/GNOME/gspell"
source = f"https://download.gnome.org/sources/gspell/1.14/gspell-{pkgver}.tar.xz"
sha256 = "788783b56fc3d03283b3aa29302d0b958aeca88835e10b1ec61f19e0efc7e8a4"
# tests need a display and installed dictionaries
options = ["!check"]


@subpackage("gspell-devel")
def _(self):
    return self.default_devel()


def post_install(self):
    self.install_license("LICENSES/LGPL-2.1-or-later.txt")
