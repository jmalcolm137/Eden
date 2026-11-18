pkgname = "libxfce4ui"
pkgver = "4.21.9"
pkgrel = 1
build_style = "meson"
configure_args = [
    "-Dx11=disabled",
    "-Dwayland=enabled",
    "-Dintrospection=false",
    "-Dvala=disabled",
    "-Dgtk-doc=false",
    "-Dkeyboard-library=true",
    "-Dsession-management=disabled",
    "-Dstartup-notification=disabled",
    "-Dlibgtop=disabled",
    "-Depoxy=disabled",
    "-Dgudev=disabled",
]
hostmakedepends = [
    "gettext",
    "glib-devel",
    "muon",
    "pkgconf",
    "python",
    "samurai",
    "wayland-progs",
    "xfce4-dev-tools",
]
makedepends = [
    "glib-devel",
    "gtk+3-devel",
    "libxfce4util-devel",
    "libxml2-devel",
    "xfconf-devel",
]
pkgdesc = "Xfce UI library"
license = "LGPL-2.0-or-later"
url = "https://docs.xfce.org/xfce/libxfce4ui/start"
source = f"https://archive.xfce.org/src/xfce/libxfce4ui/4.21/libxfce4ui-4.21.9.tar.xz"
sha256 = "d2072e0c3c27e39e1c38050c660f34806e34e8b1abba660684db586f8c4f7142"
# upstream tests need a display and a running session bus
options = ["!check", "!lintpixmaps", "etcfiles"]


@subpackage("libxfce4ui-devel")
def _(self):
    return self.default_devel()
