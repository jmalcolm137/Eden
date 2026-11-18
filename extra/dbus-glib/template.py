pkgname = "dbus-glib"
pkgver = "0.114"
pkgrel = 1
build_style = "gnu_configure"
configure_args = ["--disable-bash-completion"]
configure_gen = []
hostmakedepends = ["pkgconf"]
makedepends = ["dbus-devel", "glib-devel", "libexpat-devel"]
pkgdesc = "GLib bindings for D-Bus"
license = "AFL-2.1 OR GPL-2.0-or-later"
url = "https://www.freedesktop.org/wiki/Software/DBusBindings"
source = "https://dbus.freedesktop.org/releases/dbus-glib/dbus-glib-0.114.tar.gz"
sha256 = "c09c5c085b2a0e391b8ee7d783a1d63fe444e96717cc1814d61b5e8fc2827a7c"
# tests need a running message bus
options = ["!check"]


@subpackage("dbus-glib-devel")
def _(self):
    return self.default_devel()


def post_install(self):
    self.install_license("COPYING")
