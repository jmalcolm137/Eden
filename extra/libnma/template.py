pkgname = "libnma"
pkgver = "1.10.6"
pkgrel = 1
build_style = "meson"
configure_args = [
    "-Dgcr=false",
    "-Dgtk_doc=false",
    "-Dintrospection=false",
    "-Dlibnma_gtk4=false",
    "-Dmobile_broadband_provider_info=false",
    "-Dvapi=false",
]
hostmakedepends = ["gettext", "meson-real", "pkgconf", "samurai"]
makedepends = ["gtk+3-devel", "iso-codes", "networkmanager-devel"]
depends = ["iso-codes", "networkmanager"]
pkgdesc = "NetworkManager GUI client library for GTK"
license = "GPL-2.0-or-later AND LGPL-2.1-or-later"
url = "https://gitlab.gnome.org/GNOME/libnma"
source = f"https://download.gnome.org/sources/libnma/1.10/libnma-{pkgver}.tar.xz"
sha256 = "53a6fb2b190ad37c5986caed3e98bede7c3c602399ee4f93c8fc054303d76dab"
# tests need a display and a session bus
options = ["!check"]


@subpackage("libnma-devel")
def _(self):
    return self.default_devel()


def post_install(self):
    self.install_license("COPYING")
