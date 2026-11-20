pkgname = "exo"
pkgver = "4.21.0"
pkgrel = 0
build_style = "gnu_configure"
configure_args = [
    "--disable-static",
]
configure_gen = []
hostmakedepends = [
    "gettext",
    "glib-devel",
    "pkgconf",
    "python",
]
makedepends = [
    "glib-devel",
    "gtk+3-devel",
    "libxfce4ui-devel",
]
pkgdesc = "Xfce extensions library"
license = "GPL-2.0-or-later AND LGPL-2.1-or-later"
url = "https://docs.xfce.org/xfce/exo/start"
source = "https://archive.xfce.org/src/xfce/exo/4.21/exo-4.21.0.tar.bz2"
sha256 = "26f85ca2db3bcf99d8b8af28b0d565b0186ccc3d2ed4a5ba315f6a589b8bc2c9"
# upstream tests need a display and a running session bus
options = ["!check", "!lintpixmaps"]


@subpackage("exo-devel")
def _(self):
    return self.default_devel()
