pkgname = "xfce4-mailwatch-plugin"
pkgver = "1.4.0"
pkgrel = 0
build_style = "meson"
hostmakedepends = [
    "gettext",
    "glib-devel",
    "muon",
    "pkgconf",
    "samurai",
]
makedepends = [
    "exo-devel",
    "gnutls-devel",
    "gtk+3-devel",
    "libxfce4ui-devel",
    "libxfce4util-devel",
    "xfce4-panel-devel",
]
pkgdesc = "Xfce mail watcher panel plugin"
license = "GPL-2.0-only"
url = "https://docs.xfce.org/panel-plugins/xfce4-mailwatch-plugin/start"
source = "https://archive.xfce.org/src/panel-plugins/xfce4-mailwatch-plugin/1.4/xfce4-mailwatch-plugin-1.4.0.tar.xz"
sha256 = "5c211025db1096663fa6b8cc41213464a6d71f24e76326499d857ff81ea3861f"
# upstream tests need a display and a running session bus
options = ["!check"]
