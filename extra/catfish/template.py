pkgname = "catfish"
pkgver = "4.20.1"
pkgrel = 0
build_style = "meson"
meson_impl = "meson"
hostmakedepends = [
    "gettext",
    "glib-devel",
    "meson-real",
    "muon",
    "pkgconf",
    "python",
    "python-dbus",
    "python-gobject",
    "python-pexpect",
    "samurai",
]
makedepends = [
    "gtk+3-devel",
    "pango-devel",
    "xfconf-devel",
]
depends = [
    "gtk+3",
    "pango",
    "python-dbus",
    "python-gobject",
    "python-pexpect",
    "xfconf",
]
pkgdesc = "Xfce file search tool"
license = "GPL-2.0-or-later"
url = "https://docs.xfce.org/apps/catfish/start"
source = f"https://archive.xfce.org/src/apps/catfish/4.20/catfish-4.20.1.tar.xz"
sha256 = "fe00d45b163cf86b4c85ebdd23a73d53aa55bc97ba3f691a248ec403d4ade62b"
# upstream tests need a display and a running session bus
options = ["!check"]
