pkgname = "harfbuzz"
pkgver = "14.5.0"
pkgrel = 0
build_style = "meson"
configure_args = [
    "-Dbenchmark=disabled",
    "-Dcairo=disabled",
    "-Dchafa=disabled",
    "-Ddoc_tests=false",
    "-Ddocs=disabled",
    "-Dfontations=disabled",
    "-Dfreetype=enabled",
    "-Dglib=enabled",
    "-Dgobject=enabled",
    "-Dgpu=disabled",
    "-Dgraphite2=disabled",
    "-Dharfrust=disabled",
    "-Dicu=disabled",
    "-Dintrospection=disabled",
    "-Dkbts=disabled",
    "-Dpng=disabled",
    "-Dtests=disabled",
    "-Dutilities=disabled",
    "-Dvector=disabled",
    "-Dwasm=disabled",
    "-Dzlib=disabled",
]
hostmakedepends = [
    "glib-devel",
    "muon",
    "pkgconf",
    "python",
    "samurai",
]
makedepends = [
    "freetype-devel",
    "glib-devel",
]
pkgdesc = "OpenType text shaping engine"
license = "MIT"
url = "https://harfbuzz.github.io"
source = "https://github.com/harfbuzz/harfbuzz/releases/download/14.5.0/harfbuzz-14.5.0.tar.xz"
sha256 = "b7132e148358a45185c9feafd049dbaf243649d3c44414b3534d9c95d18592b9"
# tests require a display or a full graphics stack
options = ["!check"]


@subpackage("harfbuzz-devel")
def _(self):
    return self.default_devel()


def post_install(self):
    self.install_license("COPYING")
