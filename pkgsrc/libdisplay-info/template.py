pkgname = "libdisplay-info"
pkgver = "0.3.0"
pkgrel = 0
build_style = "meson"
hostmakedepends = [
    "muon",
    "pkgconf",
    "python",
    "samurai",
]
makedepends = [
    "hwdata-devel",
]
pkgdesc = "EDID and DisplayID parsing library"
license = "MIT"
url = "https://gitlab.freedesktop.org/emersion/libdisplay-info"
source = "https://gitlab.freedesktop.org/emersion/libdisplay-info/-/archive/0.3.0/libdisplay-info-0.3.0.tar.gz"
sha256 = "2b467e3336aec63819d6aca28d7310d3dc7415b2b3a3c3a5aec9d3727053c078"
# tests require a display or a full graphics stack
options = ["!check"]


@subpackage("libdisplay-info-devel")
def _(self):
    return self.default_devel()


def post_install(self):
    self.install_license("LICENSE")
