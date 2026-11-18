pkgname = "libgtop"
pkgver = "2.41.3"
pkgrel = 1
build_style = "gnu_configure"
configure_args = [
    "--disable-gtk-doc",
    "--disable-static",
    "--without-fp",
]
configure_gen = []
hostmakedepends = ["gettext", "libtool", "perl", "pkgconf"]
makedepends = ["glib-devel", "linux-headers"]
pkgdesc = "Library for portably obtaining system information"
license = "GPL-2.0-or-later"
url = "https://gitlab.gnome.org/GNOME/libgtop"
source = f"https://download.gnome.org/sources/libgtop/2.41/libgtop-{pkgver}.tar.xz"
sha256 = "775676df958e2ea2452f7568f28b2ea581063d312773dd5c0b7624c1b9b2da8c"
file_modes = {"usr/lib/libgtop_server2": ("root", "root", 0o4755)}
# needs a live system and its own test harness
options = ["!check"]


@subpackage("libgtop-devel")
def _(self):
    return self.default_devel()


def post_install(self):
    self.install_license("COPYING")
