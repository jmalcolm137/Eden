pkgname = "pango"
pkgver = "1.58.2"
pkgrel = 0
build_style = "meson"
configure_args = [
    "-Dbuild-examples=false",
    "-Dbuild-testsuite=false",
    "-Dcairo=enabled",
    "-Ddocumentation=false",
    "-Dfontconfig=enabled",
    "-Dfreetype=enabled",
    "-Dgtk_doc=false",
    "-Dintrospection=disabled",
    "-Dlibthai=disabled",
    "-Dman-pages=false",
    "-Dsysprof=disabled",
    "-Dxft=disabled",
]
hostmakedepends = [
    "glib-devel",
    "muon",
    "pkgconf",
    "python",
    "samurai",
]
makedepends = [
    "cairo-devel",
    "fontconfig-devel",
    "freetype-devel",
    "fribidi-devel",
    "glib-devel",
    "harfbuzz-devel",
]
pkgdesc = "Internationalized text layout and rendering library"
license = "LGPL-2.1-or-later"
url = "https://www.pango.org"
source = "https://download.gnome.org/sources/pango/1.58/pango-1.58.2.tar.xz"
sha256 = "342385b6ca3b7c73455d7c80a13b7dbe4489e00bc3bd4c5bd6ed4dce421e374a"
# tests require a display or a full graphics stack
options = ["!check"]


@subpackage("pango-devel")
def _(self):
    return self.default_devel()


def post_install(self):
    self.install_license("COPYING")
