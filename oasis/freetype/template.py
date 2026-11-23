pkgname = "freetype"
pkgver = "2.14.3"
pkgrel = 0
build_style = "meson"
configure_args = [
    "-Dbrotli=disabled",
    "-Dbzip2=disabled",
    "-Dharfbuzz=disabled",
    "-Dmmap=enabled",
    "-Dpng=disabled",
    "-Dtests=disabled",
    "-Dzlib=enabled",
]
hostmakedepends = [
    "muon",
    "pkgconf",
    "python",
    "samurai",
]
makedepends = [
    "zlib",
]
pkgdesc = "Font rendering engine"
license = "FTL OR GPL-2.0-or-later"
url = "https://freetype.org"
source = "https://downloads.sourceforge.net/sourceforge/freetype/freetype-2.14.3.tar.xz"
sha256 = "36bc4f1cc413335368ee656c42afca65c5a3987e8768cc28cf11ba775e785a5f"
# tests require a display and test fonts
options = ["!check", "!splitstatic"]


@subpackage("freetype-devel")
def _(self):
    return self.default_devel()


def post_install(self):
    self.install_license("LICENSE.TXT")
