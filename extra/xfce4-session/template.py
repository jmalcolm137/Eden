pkgname = "xfce4-session"
pkgver = "4.21.2"
pkgrel = 0
build_style = "meson"
configure_args = [
    "-Dx11=disabled",
    "-Dwayland=enabled",
    "-Dintrospection=false",
    "-Dvala=disabled",
    "-Dgtk-doc=false",
    "-Dlegacy-session-management=false",
    "-Dgtk-layer-shell=enabled",
    "-Dpolkit=enabled",
]
hostmakedepends = [
    "gettext",
    "glib-devel",
    "muon",
    "pkgconf",
    "polkit-devel",
    "samurai",
    "wayland-progs",
    "xfce4-dev-tools",
]
makedepends = [
    "glib-devel",
    "gtk+3-devel",
    "gtk-layer-shell-devel",
    "libxfce4ui-devel",
    "libxfce4util-devel",
    "libxfce4windowing-devel",
    "polkit-devel",
    "wayland-devel",
    "wayland-protocols",
    "xfconf-devel",
]
pkgdesc = "Xfce desktop session"
license = "GPL-2.0-or-later"
url = "https://docs.xfce.org/xfce/xfce4-session/start"
source = f"https://archive.xfce.org/src/xfce/xfce4-session/4.21/xfce4-session-4.21.2.tar.xz"
sha256 = "1809216cb1c658cba50c56b70bcdc1bd073bd357980a4dc335d442eb559bf18a"
# upstream tests need a display and a running session bus
options = ["!check", "etcfiles"]


def post_patch(self):
    # the settings editor only uses the XSMP names as D-Bus property names,
    # so define them locally instead of pulling in the X11 headers
    p = self.cwd / "settings/session-editor.c"
    text = p.read_text()
    old = "#include <X11/SM/SMlib.h>"
    if old not in text:
        self.error("unexpected X11 SM include in session-editor.c")
    text = text.replace(
        old,
        "\n".join(
            [
                "#define SmProcessID \"ProcessID\"",
                "#define SmProgram \"Program\"",
                "#define SmRestartStyleHint \"RestartStyleHint\"",
                "#define SmRestartIfRunning 0",
                "#define SmRestartNever 3",
            ]
        ),
    )
    p.write_text(text)


def pre_build(self):
    # muon passes the build directory as the gresource source directory, so
    # make the referenced UI file visible there
    self.cp(
        "settings/xfce4-session-settings.ui",
        "build/settings/xfce4-session-settings.ui",
    )


@subpackage("xfce4-session-devel")
def _(self):
    return self.default_devel()
