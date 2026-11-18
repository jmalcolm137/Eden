pkgname = "gst-plugins-base"
pkgver = "1.28.9"
pkgrel = 1
build_style = "meson"
configure_args = [
    "-Dalsa=disabled",
    "-Dcdparanoia=disabled",
    "-Dexamples=disabled",
    "-Dgl=disabled",
    "-Dgl-graphene=disabled",
    "-Dgl-jpeg=disabled",
    "-Dgl-png=disabled",
    "-Dintrospection=disabled",
    "-Dlibvisual=disabled",
    "-Dnls=disabled",
    "-Dogg=disabled",
    "-Dopus=disabled",
    "-Dorc=disabled",
    "-Dorc-compiler=disabled",
    "-Dpango=disabled",
    "-Dtests=disabled",
    "-Dtheora=disabled",
    "-Dtools=disabled",
    "-Dtremor=disabled",
    "-Dvorbis=disabled",
    "-Dx11=disabled",
 ]
meson_impl = "meson"
hostmakedepends = ["meson-real", "pkgconf", "python", "samurai"]
makedepends = ["glib-devel", "gstreamer-devel"]
pkgdesc = "GStreamer base plugins"
license = "LGPL-2.1-or-later"
url = "https://gstreamer.freedesktop.org"
source = "https://gstreamer.freedesktop.org/src/gst-plugins-base/gst-plugins-base-1.28.9.tar.xz"
sha256 = "c1fda668b520e6aef763c0eb962c032c9fe52bce322e8b00c69b4e9e847bddc1"
# tests and examples need the full media stack
options = ["!check"]


@subpackage("gst-plugins-base-devel")
def _(self):
    return self.default_devel()


def post_install(self):
    for f in (self.destdir / "usr/lib/gstreamer-1.0").glob("*.a"):
        f.unlink()
    self.install_license("COPYING")
