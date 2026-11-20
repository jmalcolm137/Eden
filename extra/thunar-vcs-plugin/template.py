pkgname = "thunar-vcs-plugin"
pkgver = "0.4.0"
pkgrel = 0
build_style = "meson"
configure_args = [
    "-Dsvn=disabled",
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
    "thunar-devel",
]
depends = [
    "git",
]
pkgdesc = "Version control integration for Thunar"
license = "GPL-2.0-or-later"
url = "https://docs.xfce.org/xfce/thunar/thunar-vcs-plugin"
source = "https://archive.xfce.org/src/thunar-plugins/thunar-vcs-plugin/0.4/thunar-vcs-plugin-0.4.0.tar.xz"
sha256 = "0e4170e099c9ffedfcbb1290f1fc42c00560cf6108e25fe90685315f18c8d6cc"
# upstream tests need a display and a running session bus
options = ["!check"]
