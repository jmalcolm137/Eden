pkgname = "libcanberra"
pkgver = "0.30"
pkgrel = 1
build_style = "gnu_configure"
configure_args = [
    "--disable-alsa",
    "--disable-gstreamer",
    "--disable-gtk",
    "--disable-gtk3",
    "--disable-lynx",
    "--disable-oss",
    "--disable-tdb",
]
configure_gen = []
hostmakedepends = ["file", "pkgconf"]
makedepends = [
    "glib-devel",
    "libpulse-devel",
    "libtool-devel",
    "libvorbis-devel",
    "udev-devel",
]
pkgdesc = "Event sound library"
license = "LGPL-2.1-or-later"
url = "http://0pointer.de/lennart/projects/libcanberra"
source = "http://0pointer.de/lennart/projects/libcanberra/libcanberra-0.30.tar.xz"
sha256 = "c2b671e67e0c288a69fc33dc1b6f1b534d07882c2aceed37004bf48c601afa72"
# tests need an audio stack
options = ["!check"]


@subpackage("libcanberra-devel")
def _(self):
    return self.default_devel()


def post_install(self):
    self.install_license("LGPL")
