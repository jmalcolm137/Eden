pkgname = "xfce4-power-manager"
pkgver = "4.21.1"
pkgrel = 0
build_style = "meson"
configure_args = [
    "-Dx11=disabled",
    "-Dwayland=enabled",
    "-Dpanel-plugin=enabled",
    "-Dpolkit=enabled",
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
    "glib-devel",
    "gtk+3-devel",
    "libnotify-devel",
    "libxfce4ui-devel",
    "libxfce4util-devel",
    "polkit-devel",
    "upower-devel",
    "wayland-devel",
    "wayland-protocols",
    "xfce4-panel-devel",
    "xfconf-devel",
]
depends = [
    "polkit",
]
pkgdesc = "Xfce power manager"
license = "GPL-2.0-only"
url = "https://docs.xfce.org/xfce/xfce4-power-manager/start"
source = "https://archive.xfce.org/src/xfce/xfce4-power-manager/4.21/xfce4-power-manager-4.21.1.tar.xz"
sha256 = "bb89be7b1be431b29e765e2c632e98fb20a688e495e4ef18495bd70c1524767a"
# upstream tests need a display and a running session bus
options = ["!check", "etcfiles"]


def pre_build(self):
    # muon passes the build directory as the gresource source directory
    self.cp(
        "data/interfaces/xfpm-settings.ui",
        "build/data/interfaces/xfpm-settings.ui",
    )


def post_patch(self):
    # keep the native scanner dependency out of wayland_deps; muon rejects a
    # host library depending on a build-machine dependency
    p = self.cwd / "meson.build"
    text = p.read_text()
    old = """wayland_deps += dependency('wayland-scanner', version: dependency_versions['wayland'], required: get_option('wayland'), native: true)
wayland_scanner = wayland_deps[-1]"""
    new = """wayland_scanner = dependency('wayland-scanner', version: dependency_versions['wayland'], required: get_option('wayland'), native: true)"""
    if old not in text:
        self.error("unexpected wayland-scanner dependency in meson.build")
    p.write_text(text.replace(old, new))
