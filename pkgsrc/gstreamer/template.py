pkgname = "gstreamer"
pkgver = "1.28.9"
pkgrel = 1
build_style = "meson"
configure_args = [
    "-Dbenchmarks=disabled",
    "-Ddoc=disabled",
    "-Dexamples=disabled",
    "-Dtests=disabled",
    "-Dtools=enabled",
]
hostmakedepends = ["bison", "flex", "gettext", "muon", "pkgconf", "python", "samurai"]
makedepends = ["glib-devel", "libxml2-devel"]
pkgdesc = "Streaming media framework"
license = "LGPL-2.1-or-later"
url = "https://gstreamer.freedesktop.org"
source = "https://gstreamer.freedesktop.org/src/gstreamer/gstreamer-1.28.9.tar.xz"
sha256 = "6dbf744f583131a34845cc641e803843766a9ba80ce00378a9043fd6d8d5fb38"
# tests and examples need a large media stack
options = ["!check"]


@subpackage("gstreamer-devel")
def _(self):
    return self.default_devel()


@subpackage("gstreamer-progs")
def _(self):
    return self.default_progs()


def post_install(self):
    for f in (self.destdir / "usr/lib/gstreamer-1.0").glob("*.a"):
        f.unlink()
    self.install_license("COPYING")
