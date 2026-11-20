pkgname = "xfconfd-lite"
pkgver = "4.21.2"
pkgrel = 0
build_style = "makefile"
makedepends = ["glib-devel"]
depends = ["glib"]
replaces = ["xfconf"]
pkgdesc = "Minimal org.xfce.Xfconf session daemon for Eden live images"
license = "LGPL-2.0-or-later"
url = "https://docs.xfce.org/xfce/xfconf/start"
source = f"https://archive.xfce.org/src/xfce/xfconf/4.21/xfconf-{pkgver}.tar.xz"
sha256 = "99aa4366e909ba7b9f746aba48b610b9e9d2933aeb283c7fa5f37a7c3dc7a3a6"
# standalone reimplementation; upstream tests do not apply
options = ["!check"]


def post_patch(self):
    for f in [
        "Makefile",
        "main.c",
        "xbg.c",
        "xbg.h",
        "org.xfce.Xfconf.service",
    ]:
        (self.cwd / f).write_bytes((self.files_path / f).read_bytes())
