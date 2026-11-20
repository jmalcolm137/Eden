pkgname = "parole"
pkgver = "4.20.0"
pkgrel = 0
build_style = "meson"
configure_args = [
    "-Dx11=disabled",
    "-Dwayland=enabled",
    "-Dgtk-doc=false",
]
hostmakedepends = [
    "gettext",
    "glib-devel",
    "muon",
    "pkgconf",
    "samurai",
    "wayland-progs",
]
makedepends = [
    "dbus-glib-devel",
    "glib-devel",
    "gst-plugins-base-devel",
    "gstreamer-devel",
    "gtk+3-devel",
    "libnotify-devel",
    "libxfce4ui-devel",
    "libxfce4util-devel",
    "linux-headers",
    "taglib-devel",
    "xfconf-devel",
]
pkgdesc = "Xfce media player"
license = "GPL-2.0-or-later"
url = "https://docs.xfce.org/xfce/parole/start"
source = "https://archive.xfce.org/src/apps/parole/4.20/parole-4.20.0.tar.xz"
sha256 = "5cf753e670d6518701133eb860d8bceb3a08a496af6a2b7cc67b93320230c983"
# upstream tests need a display and a running session bus
options = ["!check"]


def pre_build(self):
    # muon passes the build directory as the gresource source directory
    for f in (
        "mediachooser.ui",
        "open-location.ui",
        "parole-settings.ui",
        "parole.ui",
        "playlist.ui",
        "plugins.ui",
        "save-playlist.ui",
        "shortcuts.ui",
    ):
        self.cp(f"data/interfaces/{f}", f"build/data/interfaces/{f}")
