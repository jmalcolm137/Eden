pkgname = "thunar"
pkgver = "4.21.7"
pkgrel = 0
build_style = "meson"
configure_args = [
    "-Dx11=disabled",
    "-Dintrospection=false",
    "-Dgtk-doc=false",
    "-Dtests=false",
    "-Dsession-management=disabled",
]
hostmakedepends = [
    "gettext",
    "glib-devel",
    "libtool",
    "libxslt-progs",
    "muon",
    "pkgconf",
    "samurai",
    "wayland-progs",
    "xfce4-dev-tools",
]
makedepends = [
    "exo-devel",
    "gdk-pixbuf-devel",
    "glib-devel",
    "gtk+3-devel",
    "libgudev-devel",
    "libnotify-devel",
    "libxfce4ui-devel",
    "libxfce4util-devel",
    "pango-devel",
    "xfce4-panel-devel",
    "xfconf-devel",
]
pkgdesc = "Xfce file manager"
license = "GPL-2.0-or-later AND LGPL-2.0-or-later"
url = "https://docs.xfce.org/xfce/thunar/start"
source = "https://archive.xfce.org/src/xfce/thunar/4.21/thunar-4.21.7.tar.xz"
sha256 = "fcb196b2f89cbcb8a3f5130fa9a1a11bc49d66a6403bc91aff7676648d95d51f"
# upstream tests need a display and a running session bus
options = ["!check", "etcfiles"]


def post_patch(self):
    # the man page needs the DocBook XSL stylesheets, which are not part of
    # this tree; keep the data install and drop the xsltproc target
    p = self.cwd / "docs/meson.build"
    text = p.read_text()
    text = text[text.index("install_data(") :]
    p.write_text(text)


def pre_build(self):
    # muon passes the build directory as the gresource source directory
    for f in ("thunar-thumbnail-frame.png", "thunar-uca-editor.ui"):
        self.cp(f"thunar/{f}", f"build/thunar/{f}")


def post_install(self):
    self.uninstall("usr/lib/systemd/user", missing_ok=True)


@subpackage("thunar-devel")
def _(self):
    return self.default_devel()
