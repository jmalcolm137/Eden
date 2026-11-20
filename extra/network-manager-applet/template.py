pkgname = "network-manager-applet"
pkgver = "1.36.0"
pkgrel = 1
build_style = "meson"
configure_args = [
    "-Dappindicator=no",
    "-Dc_link_args=-Wl,--undefined-version",
    "-Dselinux=false",
    "-Dteam=false",
    "-Dwwan=false",
]
hostmakedepends = ["gettext", "meson-real", "pkgconf", "samurai"]
makedepends = [
    "gtk+3-devel",
    "libnma-devel",
    "libsecret-devel",
    "networkmanager-devel",
]
depends = ["libnma", "libsecret", "networkmanager"]
pkgdesc = "NetworkManager applet for desktops without a dedicated frontend"
license = "GPL-2.0-or-later"
url = "https://gitlab.gnome.org/GNOME/network-manager-applet"
source = f"https://download.gnome.org/sources/network-manager-applet/1.36/network-manager-applet-{pkgver}.tar.xz"
sha256 = "a84704487ea3afe1485c47fb2ab598b8f779f540ae0dcbf0a1c5f85e64a7e253"
# tests need a display and a session bus
options = ["etcfiles", "!check"]


def post_patch(self):
    # the X11 include is unused; our GTK3 has the X11 backend disabled
    for f in (
        "src/applet.h",
        "src/connection-editor/nm-connection-list.c",
        "src/connection-editor/nm-connection-editor.c",
    ):
        p = self.cwd / f
        p.write_text(
            p.read_text().replace(
                "#include <gdk/gdkx.h>",
                "#ifdef GDK_WINDOWING_X11\n#include <gdk/gdkx.h>\n#endif",
            )
        )


def post_install(self):
    self.install_license("COPYING")
