pkgname = "xkeyboard-config"
pkgver = "2.36"
pkgrel = 0
# Oasis pkg/xkeyboard-config/src
_commit = "60d5dd7bf463e5754f047cb98b17102e524e8f16"
build_style = "meson"
configure_args = [
    "-Dxkb-base=/usr/share/X11/xkb",
    "-Dxorg-rules-symlinks=true",
]
hostmakedepends = ["perl", "python"]
pkgdesc = "X keyboard configuration data"
license = "MIT"
url = "https://gitlab.freedesktop.org/xkeyboard-config/xkeyboard-config"
source = (
    f"{url}/-/archive/{_commit}/xkeyboard-config-{_commit}.tar.gz"
)
sha256 = "3dbe168828be9edf8dcb08682810e91ac661a811a113a082850ea2325b5fe52e"
# no test suite in the Oasis recipe
options = ["!check"]


def post_install(self):
    self.install_license("COPYING")
