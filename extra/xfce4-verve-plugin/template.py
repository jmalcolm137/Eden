pkgname = "xfce4-verve-plugin"
pkgver = "2.1.0"
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
    "gtk+3-devel",
    "libxfce4ui-devel",
    "pcre2-devel",
    "xfce4-panel-devel",
]
pkgdesc = "Xfce command line panel plugin"
license = "GPL-2.0-or-later"
url = "https://docs.xfce.org/panel-plugins/xfce4-verve-plugin/start"
source = f"https://archive.xfce.org/src/panel-plugins/xfce4-verve-plugin/2.1/xfce4-verve-plugin-2.1.0.tar.xz"
sha256 = "237e0da802cdc02e0ec0c3cdefecb6fa2992ade9f59ce2999779cc30d59c9f24"
# upstream tests need a display and a running session bus
options = ["!check"]


def post_patch(self):
    # the X11 headers are included without using any X11 API
    p = self.cwd / "panel-plugin/verve-plugin.c"
    text = p.read_text()
    for line in ("#include <X11/Xlib.h>\n", "#include <X11/Xatom.h>\n"):
        if line not in text:
            self.error("unexpected X11 include in verve-plugin.c")
        text = text.replace(line, "")
    p.write_text(text)
