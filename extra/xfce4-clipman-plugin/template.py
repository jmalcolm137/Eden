pkgname = "xfce4-clipman-plugin"
pkgver = "1.7.0"
pkgrel = 0
build_style = "meson"
configure_args = [
    # FIXME: libqrencode is not ported yet
    "-Dqrencode=disabled",
    "-Dx11=disabled",
    "-Dwayland=enabled",
    "-Dtests=false",
    "-Dxtst=disabled",
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
    "gtk+3-devel",
    "libxfce4ui-devel",
    "libxfce4util-devel",
    "wayland-devel",
    "xfce4-panel-devel",
    "xfconf-devel",
]
pkgdesc = "Xfce clipboard manager app and panel plugin"
license = "GPL-2.0-or-later"
url = "https://docs.xfce.org/panel-plugins/xfce4-clipman-plugin/start"
source = f"https://archive.xfce.org/src/panel-plugins/xfce4-clipman-plugin/1.7/xfce4-clipman-plugin-1.7.0.tar.xz"
sha256 = "903302c3070a951d44ee17a84fa3cf21d36c6787678af8fbfc79e469fd00cb46"
# upstream tests need a display and a running session bus
options = ["!check", "etcfiles"]


def pre_build(self):
    # muon passes the build directory as the gresource source directory
    self.cp(
        "panel-plugin/settings-dialog.ui",
        "build/panel-plugin/settings-dialog.ui",
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
