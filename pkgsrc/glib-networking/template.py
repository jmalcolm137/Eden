pkgname = "glib-networking"
pkgver = "2.80.1"
pkgrel = 1
build_style = "meson"
configure_args = [
    "-Denvironment_proxy=disabled",
    "-Dgnome_proxy=disabled",
    "-Dgnutls=enabled",
    "-Dinstalled_tests=false",
    "-Dlibproxy=disabled",
    "-Ddefault_library=shared",
    "-Dopenssl=disabled",
]
hostmakedepends = ["gettext", "meson-real", "pkgconf", "samurai"]
makedepends = ["glib-devel", "gnutls-devel"]
depends = ["gnutls"]
pkgdesc = "Network related GIO modules"
license = "LGPL-2.1-or-later"
url = "https://wiki.gnome.org/Projects/GLib"
source = f"https://download.gnome.org/sources/glib-networking/2.80/glib-networking-{pkgver}.tar.xz"
sha256 = "b80e2874157cd55071f1b6710fa0b911d5ac5de106a9ee2a4c9c7bee61782f8e"
# tests need network access
options = ["!check"]


def post_install(self):
    self.install_license("COPYING")
