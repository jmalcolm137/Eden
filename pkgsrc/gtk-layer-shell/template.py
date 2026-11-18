pkgname = "gtk-layer-shell"
pkgver = "0.10.1"
pkgrel = 0
build_style = "meson"
configure_args = [
    "-Ddocs=false",
    "-Dexamples=false",
    "-Dintrospection=false",
    "-Dtests=false",
    "-Dvapi=false",
]
hostmakedepends = [
    "muon",
    "pkgconf",
    "samurai",
    "wayland-progs",
]
makedepends = [
    "gtk+3-devel",
    "wayland-devel",
    "wayland-protocols",
]
pkgdesc = "Library to create panels and other desktop components for Wayland"
license = "LGPL-3.0-or-later AND MIT"
url = "https://github.com/wmww/gtk-layer-shell"
source = "https://github.com/wmww/gtk-layer-shell/archive/refs/tags/v0.10.1.tar.gz"
sha256 = "88c3a3e0a5300532f3d368d5df64838a87f1fb85273f22d41df0a6b8d0ec59c6"
hardening = ["!vis"]
# tests require a display or a full graphics stack
options = ["!check"]


def post_install(self):
    self.install_license("LICENSE_MIT.txt")


@subpackage("gtk-layer-shell-devel")
def _(self):
    return self.default_devel()
