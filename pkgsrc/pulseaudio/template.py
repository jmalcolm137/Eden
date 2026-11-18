pkgname = "pulseaudio"
pkgver = "17.0"
pkgrel = 1
build_style = "meson"
configure_args = [
    "-Dbashcompletiondir=no",
    "-Dc_link_args=-Wl,--undefined-version",
    "-Dadrian-aec=true",
    "-Dalsa=disabled",
    "-Dasyncns=disabled",
    "-Davahi=disabled",
    "-Dbluez5=disabled",
    "-Dbluez5-gstreamer=disabled",
    "-Dconsolekit=disabled",
    "-Ddatabase=simple",
    "-Ddbus=enabled",
    "-Ddoxygen=false",
    "-Delogind=disabled",
    "-Dfftw=disabled",
    "-Dglib=enabled",
    "-Dgsettings=disabled",
    "-Dgstreamer=disabled",
    "-Dgtk=disabled",
    "-Dhal-compat=false",
    "-Djack=disabled",
    "-Dlirc=disabled",
    "-Dman=false",
    "-Dopenssl=disabled",
    "-Dorc=disabled",
    "-Doss-output=disabled",
    "-Dsamplerate=disabled",
    "-Dsoxr=disabled",
    "-Dspeex=disabled",
    "-Dsystemd=disabled",
    "-Dtcpwrap=disabled",
    "-Dtests=false",
    "-Dudev=enabled",
    "-Dvalgrind=disabled",
    "-Dwebrtc-aec=disabled",
    "-Dx11=disabled",
    "-Dzshcompletiondir=no",
]
meson_impl = "meson"
hostmakedepends = ["gettext", "meson-real", "pkgconf", "samurai"]
makedepends = [
    "dbus-devel",
    "glib-devel",
    "libsndfile-devel",
    "libtool-devel",
    "udev-devel",
]
depends = ["libtool-libs"]
pkgdesc = "Sound server for POSIX and Win32 systems"
license = "LGPL-2.1-or-later"
url = "https://www.freedesktop.org/wiki/Software/PulseAudio"
source = f"https://freedesktop.org/software/pulseaudio/releases/pulseaudio-{pkgver}.tar.xz"
sha256 = "053794d6671a3e397d849e478a80b82a63cb9d8ca296bd35b73317bb5ceb87b5"
# tests need a running daemon
options = ["!check", "etcfiles"]


@subpackage("libpulse")
def _(self):
    self.provides = [self.with_pkgver("pulseaudio-libs")]
    return self.default_libs()


@subpackage("libpulse-devel")
def _(self):
    self.provides = [self.with_pkgver("pulseaudio-devel")]
    return self.default_devel()


@subpackage("pulseaudio-progs")
def _(self):
    return self.default_progs()


def post_install(self):
    self.install_license("LICENSE")
