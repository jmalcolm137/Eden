pkgname = "upower"
pkgver = "1.91.2"
pkgrel = 1
build_style = "meson"
configure_args = [
    "-Dgtk-doc=false",
    "-Didevice=disabled",
    "-Dinstalled_tests=false",
    "-Dintrospection=disabled",
    "-Dman=false",
    "-Dpolkit=disabled",
    "-Dsystemdsystemunitdir=no",
]
hostmakedepends = ["gettext", "muon", "pkgconf", "samurai"]
makedepends = ["dbus-devel", "glib-devel", "libgudev-devel", "linux-headers"]
pkgdesc = "Power management library"
license = "GPL-2.0-or-later"
url = "https://upower.freedesktop.org"
source = "https://gitlab.freedesktop.org/upower/upower/-/archive/v1.91.2/upower-v1.91.2.tar.bz2"
sha256 = "f07f19b78a43a5053973d95a2fe96a12ede270b8db232b2e2c4ac4186fb42539"
# tests need a running daemon and hardware
options = ["etcfiles", "!check"]


@subpackage("upower-libs")
def _(self):
    return self.default_libs()


@subpackage("upower-devel")
def _(self):
    return self.default_devel()


def post_install(self):
    self.install_license("COPYING")
