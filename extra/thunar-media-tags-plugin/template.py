pkgname = "thunar-media-tags-plugin"
pkgver = "0.6.0"
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
    "glib-devel",
    "gtk+3-devel",
    "libxfce4ui-devel",
    "taglib-devel",
    "thunar-devel",
]
pkgdesc = "Media tags support for Thunar"
license = "GPL-2.0-or-later"
url = "https://docs.xfce.org/xfce/thunar/thunar-media-tags-plugin"
source = "https://archive.xfce.org/src/thunar-plugins/thunar-media-tags-plugin/0.6/thunar-media-tags-plugin-0.6.0.tar.xz"
sha256 = "b62dc047100346324e63d46acaaa497e8d7fccd1d10ef5bfb8370fd666a48c4a"
# upstream tests need a display and a running session bus
options = ["!check"]
