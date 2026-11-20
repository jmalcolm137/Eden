pkgname = "mousepad"
pkgver = "0.7.0"
pkgrel = 0
build_style = "meson"
hostmakedepends = [
    "gettext",
    "glib-devel",
    "muon",
    "pkgconf",
    "samurai",
]
makedepends = [
    "glib-devel",
    "gspell-devel",
    "gtk+3-devel",
    "gtksourceview4-devel",
    "libxfce4ui-devel",
    "polkit-devel",
]
pkgdesc = "Xfce text editor"
license = "GPL-2.0-or-later"
url = "https://docs.xfce.org/apps/mousepad/start"
source = "https://archive.xfce.org/src/apps/mousepad/0.7/mousepad-0.7.0.tar.xz"
sha256 = "e86c59feb08126d4cace368432c16b2dee8e519aaca8a9d2b409ae1cdd200802"
# upstream tests need a display and a running session bus
options = ["!check"]


def post_install(self):
    # the static helper archive is not used by anything outside the build
    self.uninstall("usr/lib/libmousepad.a")
