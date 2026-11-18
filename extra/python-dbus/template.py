pkgname = "python-dbus"
pkgver = "1.5.1"
pkgrel = 1
build_style = "meson"
configure_args = [
    "-Ddoc=disabled",
    "-Dpython=/usr/bin/python3",
    "-Dtests=disabled",
]
meson_impl = "meson"
hostmakedepends = [
    "meson-real",
    "pkgconf",
    "python",
    "samurai",
]
makedepends = ["dbus-devel", "glib-devel", "python-devel"]
depends = ["python"]
pkgdesc = "Python bindings for D-Bus"
license = "MIT"
url = "https://www.freedesktop.org/wiki/Software/DBusBindings"
source = "https://files.pythonhosted.org/packages/f3/cc/23f24bc7cbfec3a0ab508b7e11bc98837d77a91445d5f666a8545353a147/dbus_python-1.5.1.tar.gz"
sha256 = "57423cf87d09b7d084f420b55b737fe654c33339b06df77945620d97795c6ac4"
# tests need a running message bus
options = ["!check"]


def post_install(self):
    self.install_license("COPYING")
