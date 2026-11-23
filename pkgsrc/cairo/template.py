pkgname = "cairo"
pkgver = "1.18.6"
pkgrel = 0
build_style = "meson"
configure_args = [
    "-Dfontconfig=enabled",
    "-Dfreetype=enabled",
    "-Dglib=enabled",
    "-Dgtk2-utils=disabled",
    "-Ddefault_library=shared",
    "-Dgtk_doc=false",
    "-Dlzo=disabled",
    "-Dpng=enabled",
    "-Dspectre=disabled",
    "-Dsymbol-lookup=disabled",
    "-Dtests=disabled",
    "-Dxcb=disabled",
    "-Dxlib-xcb=disabled",
    "-Dxlib=disabled",
    "-Dzlib=enabled",
]
hostmakedepends = [
    "muon",
    "pkgconf",
    "python",
    "samurai",
]
makedepends = [
    "fontconfig-devel",
    "freetype-devel",
    "glib-devel",
    "libpng-devel",
    "pixman-devel",
    "zlib",
]
pkgdesc = "2D graphics library"
license = "LGPL-2.1-or-later OR MPL-1.1"
url = "https://cairographics.org"
source = "https://cairographics.org/releases/cairo-1.18.6.tar.xz"
sha256 = "1c767308174337a74694da0f3ec069c271452163a1ef4540964c50c301f157d4"
# tests require a display or a full graphics stack
options = ["!check"]


@subpackage("cairo-devel")
def _(self):
    return self.default_devel()


def post_install(self):
    self.install_license("COPYING")
