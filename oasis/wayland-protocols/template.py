pkgname = "wayland-protocols"
pkgver = "1.49"
pkgrel = 0
build_style = "meson"
configure_args = [
    "-Dtests=false",
]
hostmakedepends = [
    "muon",
    "pkgconf",
    "samurai",
    "wayland-progs",
]
makedepends = [
    "wayland-devel",
]
pkgdesc = "Wayland protocol specifications"
license = "MIT"
url = "https://wayland.freedesktop.org"
source = "https://gitlab.freedesktop.org/wayland/wayland-protocols/-/archive/1.49/wayland-protocols-1.49.tar.gz"
sha256 = "8d94eee148db4d8111ccc0d4331de2f82d4b28c38e30eace9f052886480f7d86"
# tests require a display or a full graphics stack
options = ["!check"]


def post_install(self):
    self.install_license("COPYING")
