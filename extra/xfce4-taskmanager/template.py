pkgname = "xfce4-taskmanager"
pkgver = "1.6.0"
pkgrel = 0
build_style = "meson"
configure_args = [
    "-Dx11=disabled",
    "-Dwnck=disabled",
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
    "glib-devel",
    "gtk+3-devel",
    "libxfce4ui-devel",
    "xfconf-devel",
]
pkgdesc = "Xfce task manager"
license = "GPL-2.0-or-later"
url = "https://docs.xfce.org/apps/xfce4-taskmanager/start"
source = f"https://archive.xfce.org/src/apps/xfce4-taskmanager/1.6/xfce4-taskmanager-1.6.0.tar.xz"
sha256 = "29bdc7840ab8b9025f6c0e456a83a31090d1c9fd9e26b359baa4a4010cfb0b90"
# upstream tests need a display and a running session bus
options = ["!check"]


def pre_build(self):
    # muon passes the build directory as the gresource source directory
    for f in ("process-window.ui", "settings-dialog.ui"):
        self.cp(f"src/{f}", f"build/src/{f}")


def post_patch(self):
    # libxmu is only used by the X11 window picker
    p = self.cwd / "meson.build"
    text = p.read_text()
    old = "libxmu = dependency('xmu', version: dependency_versions['libxmu'])"
    new = "libxmu = dependency('xmu', version: dependency_versions['libxmu'], required: false)"
    if old not in text:
        self.error("unexpected libxmu dependency in meson.build")
    p.write_text(text.replace(old, new))
