pkgname = "pipewire"
pkgver = "1.6.11"
pkgrel = 0
archs = ["x86_64"]
build_style = "meson"
configure_args = [
    "-Dalsa=enabled",
    "-Davahi=disabled",
    "-Dbluez5=disabled",
    "-Ddbus=enabled",
    "-Ddocs=disabled",
    "-Dexamples=disabled",
    "-Dffmpeg=disabled",
    "-Dgstreamer=disabled",
    "-Dinstalled_tests=disabled",
    "-Djack=disabled",
    "-Dlibcamera=disabled",
    "-Dlibsystemd=disabled",
    "-Dlibusb=disabled",
    "-Dman=disabled",
    "-Dpipewire-jack=disabled",
    "-Dreadline=disabled",
    "-Dsdl2=disabled",
    "-Dselinux=disabled",
    "-Dsndfile=disabled",
    "-Dsystemd-system-service=disabled",
    "-Dsystemd-user-service=disabled",
    "-Dtests=disabled",
    "-Dudev=enabled",
    "-Dvulkan=disabled",
    "-Dx11=disabled",
]
hostmakedepends = ["meson-real", "pkgconf", "python", "samurai"]
makedepends = ["alsa-lib-devel", "dbus-devel", "udev-devel"]
pkgdesc = "Multimedia framework for audio and video"
license = "MIT"
url = "https://pipewire.org"
source = f"https://github.com/PipeWire/pipewire/archive/refs/tags/{pkgver}.tar.gz"
sha256 = "f3f70c4af173cc93d05070a9d412efe3ef5889bdf4ac32298e2c0d9ae1350559"
# upstream tests need a running session and real audio devices
options = ["!check"]


@subpackage("pipewire-devel")
def _(self):
    return self.default_devel()


def post_install(self):
    self.install_license("LICENSE")
