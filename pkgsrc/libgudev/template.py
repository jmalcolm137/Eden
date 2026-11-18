pkgname = "libgudev"
pkgver = "238"
pkgrel = 1
build_style = "meson"
hostmakedepends = ["muon", "pkgconf", "samurai"]
makedepends = ["glib-devel", "udev-devel"]
pkgdesc = "GObject bindings for libudev"
license = "LGPL-2.1-or-later"
url = "https://wiki.gnome.org/Projects/libgudev"
source = "https://download.gnome.org/sources/libgudev/238/libgudev-238.tar.xz"
sha256 = "61266ab1afc9d73dbc60a8b2af73e99d2fdff47d99544d085760e4fa667b5dd1"
# tests need a running udev
options = ["!check"]


@subpackage("libgudev-devel")
def _(self):
    return self.default_devel()


def post_install(self):
    self.install_license("COPYING")


def post_patch(self):
    p = self.cwd / "gudev/meson.build"
    text = p.read_text().replace("'-export-dynamic'", "'-Wl,--export-dynamic'")
    p.write_text(text)
