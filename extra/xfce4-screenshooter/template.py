pkgname = "xfce4-screenshooter"
pkgver = "1.11.3"
pkgrel = 0
build_style = "meson"
configure_args = [
    "-Dx11=disabled",
    "-Dwayland=enabled",
    "-Dxfixes=disabled",
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
    "exo-devel",
    "gtk+3-devel",
    "libxfce4ui-devel",
    "libxfce4util-devel",
    "pango-devel",
    "wayland-devel",
    "wayland-protocols",
    "xfce4-panel-devel",
    "xfconf-devel",
]
pkgdesc = "Xfce screenshot app"
license = "GPL-2.0-or-later"
url = "https://docs.xfce.org/apps/xfce4-screenshooter/start"
source = "https://archive.xfce.org/src/apps/xfce4-screenshooter/1.11/xfce4-screenshooter-1.11.3.tar.xz"
sha256 = "1f6a14f7d1b0c440f31e24a8cc4fe2996185357fa786f0c2cdfe564ef673a710"
# upstream tests need a display and a running session bus
options = ["!check"]


def post_patch(self):
    # keep the native scanner dependency out of wayland_deps; muon rejects a
    # host library depending on a build-machine dependency
    p = self.cwd / "meson.build"
    text = p.read_text()
    old = "wayland_deps = [gdk_wayland, gtk_layer_shell, wayland_client, wayland_scanner, wayland_protocols]"
    new = "wayland_deps = [gdk_wayland, gtk_layer_shell, wayland_client, wayland_protocols]"
    if old not in text:
        self.error("unexpected wayland-scanner dependency in meson.build")
    p.write_text(text.replace(old, new))
