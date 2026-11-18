pkgname = "tumbler"
pkgver = "4.21.1"
pkgrel = 0
build_style = "meson"
configure_args = [
    "-Dcover-thumbnailer=disabled",
    "-Dgtk-doc=false",
    "-Dgepub-thumbnailer=disabled",
    "-Dgst-thumbnailer=disabled",
    "-Dodf-thumbnailer=disabled",
    "-Dpoppler-thumbnailer=disabled",
    "-Draw-thumbnailer=disabled",
    "-Dffmpeg-thumbnailer=disabled",
]
hostmakedepends = [
    "gettext",
    "glib-devel",
    "muon",
    "pkgconf",
    "samurai",
    "xfce4-dev-tools",
]
makedepends = [
    "freetype-devel",
    "gdk-pixbuf-devel",
    "glib-devel",
    "libjpeg-turbo-devel",
    "libpng-devel",
    "libxfce4util-devel",
]
pkgdesc = "Xfce implementation of the thumbnail management D-Bus spec"
license = "GPL-2.0-or-later"
url = "https://docs.xfce.org/xfce/tumbler/start"
source = f"https://archive.xfce.org/src/xfce/tumbler/4.21/tumbler-4.21.1.tar.xz"
sha256 = "0f499f79a2a7ee49726a433584dd8a680d514101b72bd1b003360611ce1dc244"
# upstream tests need a display and a running session bus
options = ["!check", "etcfiles"]


def post_install(self):
    self.uninstall("usr/lib/systemd/user", missing_ok=True)


@subpackage("tumbler-devel")
def _(self):
    return self.default_devel()
