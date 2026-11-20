pkgname = "xfce4-pulseaudio-plugin"
pkgver = "0.5.1"
pkgrel = 0
build_style = "meson"
configure_args = [
    "-Dkeybinder=disabled",
]
hostmakedepends = [
    "gettext",
    "glib-devel",
    "muon",
    "pkgconf",
    "samurai",
]
makedepends = [
    "exo-devel",
    "gtk+3-devel",
    "libcanberra-devel",
    "libnotify-devel",
    "libpulse-devel",
    "libxfce4ui-devel",
    "libxfce4util-devel",
    "libxfce4windowing-devel",
    "xfce4-panel-devel",
    "xfconf-devel",
]
# FIXME: pavucontrol needs the gtkmm-3 stack, not ported yet
# depends = ["pavucontrol"]
pkgdesc = "Xfce pulseaudio panel plugin"
license = "GPL-2.0-or-later"
url = "https://docs.xfce.org/panel-plugins/xfce4-pulseaudio-plugin/start"
source = "https://archive.xfce.org/src/panel-plugins/xfce4-pulseaudio-plugin/0.5/xfce4-pulseaudio-plugin-0.5.1.tar.xz"
sha256 = "8e1f3a505f37aa3bc2816a58bec5f9555366f1c476f10eab59fd0e6581d08c47"
# upstream tests need a display and a running session bus
options = ["!check"]


def pre_build(self):
    # muon passes the build directory as the gresource source directory
    self.cp(
        "panel-plugin/pulseaudio-dialog.glade",
        "build/panel-plugin/pulseaudio-dialog.glade",
    )
