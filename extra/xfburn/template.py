pkgname = "xfburn"
pkgver = "0.8.0"
pkgrel = 0
build_style = "meson"
hostmakedepends = [
    "gettext",
    "glib-devel",
    "libxslt-progs",
    "muon",
    "pkgconf",
    "samurai",
]
makedepends = [
    "exo-devel",
    "glib-devel",
    "gst-plugins-base-devel",
    "gstreamer-devel",
    "gtk+3-devel",
    "libburn-devel",
    "libgudev-devel",
    "libisofs-devel",
    "libxfce4ui-devel",
]
pkgdesc = "Xfce burning software"
license = "GPL-2.0-or-later"
url = "https://docs.xfce.org/apps/xfburn/start"
source = "https://archive.xfce.org/src/apps/xfburn/0.8/xfburn-0.8.0.tar.bz2"
sha256 = "13a301aebcef27de18f63f8ca10b43bc42f9c1b9865dff1bfb3e97cfd95dd989"
# upstream tests need a display and a running session bus
options = ["!check"]


def post_patch(self):
    # the man page needs the DocBook XSL stylesheets, which are not part of
    # this tree; drop the xsltproc target
    p = self.cwd / "docs/meson.build"
    p.write_text("")
