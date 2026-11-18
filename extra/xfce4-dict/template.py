pkgname = "xfce4-dict"
pkgver = "0.8.10"
pkgrel = 0
build_style = "meson"
configure_args = [
    "-Dllm=false",
]
hostmakedepends = [
    "gettext",
    "glib-devel",
    "muon",
    "pkgconf",
    "samurai",
]
makedepends = [
    "glib-devel",
    "gtk+3-devel",
    "libxfce4ui-devel",
    "libxfce4util-devel",
    "xfce4-panel-devel",
]
pkgdesc = "Xfce dictionary search app"
license = "GPL-2.0-or-later"
url = "https://docs.xfce.org/apps/xfce4-dict/start"
source = f"https://archive.xfce.org/src/apps/xfce4-dict/0.8/xfce4-dict-0.8.10.tar.xz"
sha256 = "0a0be97fd056a528a1f37c8db05f5385ffc3dc9945b424cdafa05caf5f054b67"
# upstream tests need a display and a running session bus
options = ["!check"]
