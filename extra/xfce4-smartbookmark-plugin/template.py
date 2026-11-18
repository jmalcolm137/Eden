pkgname = "xfce4-smartbookmark-plugin"
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
    "libxfce4ui-devel",
    "xfce4-panel-devel",
]
pkgdesc = "Xfce browser search panel plugin"
license = "GPL-2.0-or-later"
url = "https://docs.xfce.org/panel-plugins/xfce4-smartbookmark-plugin/start"
source = f"https://archive.xfce.org/src/panel-plugins/xfce4-smartbookmark-plugin/0.6/xfce4-smartbookmark-plugin-0.6.0.tar.xz"
sha256 = "d8a619dcad703071f7fcda538cc34154f9952cf4ec0816df23a56e98e3cc05d8"
# upstream tests need a display and a running session bus
options = ["!check"]


def post_patch(self):
    # gdkx.h is included without using any X11 API
    p = self.cwd / "src/smartbookmark.c"
    text = p.read_text()
    old = "#include <gdk/gdkx.h>\n"
    if old not in text:
        self.error("unexpected gdkx.h include in smartbookmark.c")
    p.write_text(text.replace(old, ""))
