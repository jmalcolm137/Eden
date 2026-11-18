pkgname = "gigolo"
pkgver = "0.6.0"
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
    "gtk+3-devel",
]
pkgdesc = "Xfce GIO/GVFS frontend"
license = "GPL-2.0-only"
url = "https://docs.xfce.org/apps/gigolo/start"
source = f"https://archive.xfce.org/src/apps/gigolo/0.6/gigolo-0.6.0.tar.xz"
sha256 = "f27dbb51abe8144c1b981f2d820ad1b279c1bc4623d7333b7d4f5f4777eb45ed"
# upstream tests need a display and a running session bus
options = ["!check"]


def pre_build(self):
    # muon passes the build directory as the gresource source directory
    self.cp("src/gigolo.ui", "build/src/gigolo.ui")
