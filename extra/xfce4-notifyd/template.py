pkgname = "xfce4-notifyd"
pkgver = "0.9.7"
pkgrel = 0
build_style = "meson"
configure_args = [
    "-Dx11=disabled",
    "-Dwayland=enabled",
    "-Dtests=false",
    "-Dsound=disabled",
    "-Dsystemd=disabled",
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
    "dbus-devel",
    "glib-devel",
    "gtk+3-devel",
    "gtk-layer-shell-devel",
    "libnotify-devel",
    "libxfce4ui-devel",
    "libxfce4util-devel",
    "sqlite-devel",
    "xfce4-panel-devel",
    "xfconf-devel",
]
pkgdesc = "Xfce notification daemon"
license = "GPL-2.0-only"
url = "https://docs.xfce.org/apps/xfce4-notifyd/start"
source = f"https://archive.xfce.org/src/apps/xfce4-notifyd/0.9/xfce4-notifyd-0.9.7.tar.bz2"
sha256 = "170d18fd5f40cce823ffc7ae3d7e21644007c3f45808ab4835f0401d21b3516a"
# upstream tests need a display and a running session bus
options = ["!check", "etcfiles"]


def post_patch(self):
    # socket embedding is X11-only; always use the normal dialog path
    p = self.cwd / "xfce4-notifyd-config/main.c"
    text = p.read_text().replace("#include <gtk/gtkx.h>\n", "")
    start = text.index("    if(opt_socket_id) {")
    marker = "    } else {"
    end = text.index(marker, start) + len(marker)
    text = text[:start] + "    if (1) {\n" + text[end:]
    p.write_text(text)


def pre_build(self):
    # muon passes the build directory as the gresource source directory
    for f in (
        "xfce4-notifyd-config/xfce4-notifyd-config.glade",
        "xfce4-notifyd-config/xfce4-notifyd-config-known-app.glade",
        "panel-plugin/notification-plugin-settings.glade",
    ):
        self.cp(f, f"build/{f}")
