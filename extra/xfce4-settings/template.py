pkgname = "xfce4-settings"
pkgver = "4.21.3"
pkgrel = 0
build_style = "meson"
configure_args = [
    "-Dx11=disabled",
    "-Dwayland=enabled",
    "-Dlibnotify=disabled",
    "-Dlibxklavier=disabled",
    "-Dxcursor=disabled",
    "-Dxorg-libinput=disabled",
    "-Dxrandr=disabled",
    "-Dgtk-layer-shell=enabled",
    "-Dupower=enabled",
    "-Dcolord=disabled",
    "-Dsound-settings=false",
]
hostmakedepends = [
    "gettext",
    "glib-devel",
    "libxml2-progs",
    "muon",
    "pkgconf",
    "samurai",
    "wayland-progs",
]
makedepends = [
    "exo-devel",
    "fontconfig-devel",
    "garcon-devel",
    "glib-devel",
    "gtk+3-devel",
    "gtk-layer-shell-devel",
    "libxfce4ui-devel",
    "libxfce4util-devel",
    "upower-devel",
    "wayland-devel",
    "wayland-protocols",
    "xfconf-devel",
]
pkgdesc = "Xfce settings app"
license = "GPL-2.0-only"
url = "https://docs.xfce.org/xfce/xfce4-settings/start"
source = f"https://archive.xfce.org/src/xfce/xfce4-settings/4.21/xfce4-settings-4.21.3.tar.xz"
sha256 = "2f620939359dc9737800adfcb88fa86cad89b02d83f182ad1704bbebcd86b609"
# upstream tests need a display and a running session bus
def post_patch(self):
    # keep the native scanner dependency out of wayland_deps; muon rejects a
    # host static library depending on a build-machine dependency
    p = self.cwd / "meson.build"
    text = p.read_text()
    old = """wayland_deps += dependency('wayland-scanner', version: dependency_versions['wayland'], required: get_option('wayland'), native: true)
wayland_scanner = wayland_deps[-1]"""
    new = """wayland_scanner = dependency('wayland-scanner', version: dependency_versions['wayland'], required: get_option('wayland'), native: true)"""
    if old not in text:
        self.error("unexpected wayland-scanner dependency in meson.build")
    p.write_text(text.replace(old, new))


options = ["!check", "etcfiles"]
