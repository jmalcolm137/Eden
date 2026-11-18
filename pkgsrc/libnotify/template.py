pkgname = "libnotify"
pkgver = "0.8.4"
pkgrel = 1
build_style = "meson"
configure_args = [
    "-Ddocbook_docs=disabled",
    "-Dgtk_doc=false",
    "-Dintrospection=disabled",
    "-Dman=false",
    "-Dtests=false",
]
hostmakedepends = ["muon", "pkgconf", "samurai"]
makedepends = ["gdk-pixbuf-devel", "glib-devel"]
pkgdesc = "Desktop notification framework"
license = "LGPL-2.1-or-later"
url = "https://gitlab.gnome.org/GNOME/libnotify"
source = "https://download.gnome.org/sources/libnotify/0.8/libnotify-0.8.4.tar.xz"
sha256 = "8fa04d4ebdc155b0a239df88bd9f09e8f2739d5707a1390b427ab4985f83d25a"
# tests need a running session bus
options = ["!check"]


@subpackage("libnotify-devel")
def _(self):
    return self.default_devel()


def post_install(self):
    pc = self.destdir / "usr/lib/pkgconfig/libnotify.pc"
    text = pc.read_text().replace('-DG_LOG_DOMAIN="libnotify" ', "")
    text = text.replace("-DG_LOG_DOMAIN=libnotify ", "")
    pc.write_text(text)
    self.install_license("COPYING")
