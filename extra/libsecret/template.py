pkgname = "libsecret"
pkgver = "0.21.7"
pkgrel = 1
build_style = "meson"
configure_args = [
    "-Dbash_completion=disabled",
    "-Dcrypto=gnutls",
    "-Dgtk_doc=false",
    "-Dintrospection=false",
    "-Dmanpage=false",
    "-Dpam=false",
    "-Dtpm2=false",
    "-Dvapi=false",
]
hostmakedepends = ["gettext", "meson-real", "pkgconf", "samurai"]
makedepends = ["glib-devel", "gnutls-devel", "linux-headers"]
pkgdesc = "Library for storing and retrieving passwords and secrets"
license = "LGPL-2.1-or-later"
url = "https://wiki.gnome.org/Projects/Libsecret"
source = f"https://download.gnome.org/sources/libsecret/0.21/libsecret-{pkgver}.tar.xz"
sha256 = "6b452e4750590a2b5617adc40026f28d2f4903de15f1250e1d1c40bfd68ed55e"
# tests need a running secret service
options = ["!check"]


@subpackage("libsecret-devel")
def _(self):
    return self.default_devel()


def post_install(self):
    self.install_license("COPYING")
