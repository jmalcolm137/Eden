pkgname = "libinput"
pkgver = "1.19.3"
pkgrel = 0
# Oasis pkg/libinput/src
_commit = "702610db1c4c1e14c87dbd30380f89b48c50b841"
build_style = "meson"
configure_args = [
    "-Dudev=false",
    "-Dlibwacom=false",
    "-Ddebug-gui=false",
    "-Dtests=false",
    "-Ddocumentation=false",
    "-Dtools=false",
]
makedepends = ["libevdev-devel", "linux-headers", "mtdev-devel"]
pkgdesc = "Input device handling library"
license = "MIT"
url = "https://github.com/oasislinux/libinput"
source = f"{url}/archive/{_commit}.tar.gz"
sha256 = "eb72e56fcb4dae2b1d36f46801f00429c0541ee1113fa2b94581a33acf634def"
# no test suite in the Oasis recipe
options = ["!check"]


@subpackage("libinput-devel")
def _(self):
    return self.default_devel()


def post_install(self):
    self.install_license("COPYING")
    self.uninstall("usr/share/zsh", missing_ok=True)
    self.uninstall("usr/share/bash-completion", missing_ok=True)
