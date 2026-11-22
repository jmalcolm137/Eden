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
    "-Dfftw=disabled",
    "-Dopus=disabled",
    "-Dlibpulse=disabled",
    "-Dx11-xfixes=disabled",
    "-Dlibcanberra=disabled",
    "-Dgsettings=disabled",
    "-Dflatpak=disabled",
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
    "-Dsession-managers=[]",
    "-Dsndfile=disabled",
    "-Dsystemd-system-service=disabled",
    "-Dsystemd-user-service=disabled",
    "-Dtests=disabled",
    "-Dudev=enabled",
    "-Dvulkan=disabled",
    "-Dx11=disabled",
]
hostmakedepends = ["meson-real", "pkgconf", "python", "samurai"]
makedepends = ["alsa-lib-devel", "dbus-devel", "linux-headers", "udev-devel"]
depends = ["perp"]
pkgdesc = "Multimedia framework for audio and video"
license = "MIT"
url = "https://pipewire.org"
source = f"https://github.com/PipeWire/pipewire/archive/refs/tags/{pkgver}.tar.gz"
sha256 = "f3f70c4af173cc93d05070a9d412efe3ef5889bdf4ac32298e2c0d9ae1350559"
# upstream tests need a running session and real audio devices
options = ["!check", "etcfiles"]


@subpackage("pipewire-devel")
def _(self):
    return self.default_devel()


def post_install(self):
    self.install_file(self.files_path / "pipewire-perp", "usr/bin", mode=0o755)
    for svc in ["pipewire", "pipewire-pulse"]:
        self.install_file(
            self.files_path / f"perp/{svc}/rc.main",
            f"usr/share/pipewire/perp/{svc}",
            mode=0o755,
        )
    self.install_file(
        self.files_path / "pipewire-perp.desktop", "etc/xdg/autostart"
    )


    for svc in ["pipewire", "pipewire-pulse"]:
        (self.destdir / f"usr/share/pipewire/perp/{svc}").chmod(0o1755)
    self.install_license("LICENSE")