pkgname = "python-gobject"
pkgver = "3.58.0"
pkgrel = 1
build_style = "meson"
configure_args = [
    "-Dpycairo=disabled",
    "-Dtests=false",
]
meson_impl = "meson"
hostmakedepends = [
    "meson-real",
    "pkgconf",
    "python",
    "samurai",
]
makedepends = [
    "glib-devel",
    "gobject-introspection-devel",
    "python-devel",
]
depends = ["gobject-introspection-libs", "python"]
pkgdesc = "Python bindings for GObject"
license = "LGPL-2.1-or-later"
url = "https://pygobject.readthedocs.io"
source = "https://download.gnome.org/sources/pygobject/3.58/pygobject-3.58.0.tar.gz"
sha256 = "45068697de3ffe46840ca369705f23118b34db4f7deb63f6eff079a6734ddcca"
# tests need a display and the full introspection stack
options = ["!check"]


def post_install(self):
    self.install_license("COPYING")
