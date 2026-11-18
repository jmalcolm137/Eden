pkgname = "xfdesktop"
pkgver = "4.21.1"
pkgrel = 0
build_style = "meson"
configure_args = [
    "-Dx11=disabled",
    "-Dwayland=enabled",
    "-Dtests=false",
    "-Ddesktop-menu=enabled",
    "-Ddesktop-icons=true",
    "-Dfile-icons=true",
    "-Dthunarx=enabled",
    "-Dnotifications=enabled",
    "-Dvideo-backdrop=false",
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
    "cairo-devel",
    "exo-devel",
    "garcon-devel",
    "glib-devel",
    "gtk+3-devel",
    "gtk-layer-shell-devel",
    "libnotify-devel",
    "libxfce4ui-devel",
    "libxfce4util-devel",
    "libxfce4windowing-devel",
    "libyaml-devel",
    "thunar-devel",
    "xfce4-session-devel",
    "xfconf-devel",
]
pkgdesc = "Xfce desktop manager"
license = "GPL-2.0-or-later"
url = "https://docs.xfce.org/xfce/xfdesktop/start"
source = f"https://archive.xfce.org/src/xfce/xfdesktop/4.21/xfdesktop-4.21.1.tar.xz"
sha256 = "a1b798d045c8b188af49503e2b015632b460cd179e1893cb3d2eec93eb59a33f"
# upstream tests need a display and a running session bus
def post_patch(self):
    # windowlist.c includes gdkx.h without using any X11 API
    p = self.cwd / "src/windowlist.c"
    text = p.read_text()
    old = "#include <gdk/gdkx.h>\n"
    if old not in text:
        self.error("unexpected gdkx.h include in windowlist.c")
    p.write_text(text.replace(old, ""))


def pre_build(self):
    # muon passes the build directory as the gresource source directory
    for src in (
        "settings/xfdesktop-settings-ui.glade",
        "settings/xfdesktop-settings-appearance-frame-ui.glade",
        "src/xfdesktop-monitor-chooser-ui.glade",
    ):
        self.cp(src, f"build/{src}")


options = ["!check", "!lintpixmaps"]
