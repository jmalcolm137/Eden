pkgname = "gtk+3"
pkgver = "3.24.43"
pkgrel = 0
build_style = "meson"
configure_args = [
    "-Dbroadway_backend=false",
    "-Dcloudproviders=false",
    "-Dcolord=no",
    "-Ddemos=false",
    "-Dexamples=false",
    "-Dgtk_doc=false",
    "-Dinstalled_tests=false",
    "-Dintrospection=false",
    "-Dman=false",
    "-Dprint_backends=file",
    "-Dprofiler=false",
    "-Dquartz_backend=false",
    "-Dtests=false",
    "-Dtracker3=false",
    "-Dwayland_backend=true",
    "-Dwin32_backend=false",
    "-Dx11_backend=false",
    "-Dxinerama=no",
]
hostmakedepends = [
    "gettext",
    "glib-devel",
    "muon",
    "perl",
    "pkgconf",
    "python",
    "samurai",
    "wayland-progs",
]
makedepends = [
    "atk-devel",
    "cairo-devel",
    "fribidi-devel",
    "gdk-pixbuf-devel",
    "glib-devel",
    "libepoxy-devel",
    "libxkbcommon-devel",
    "linux-headers",
    "pango-devel",
    "wayland-devel",
    "wayland-protocols",
]
depends = [
    "adwaita-icon-theme",
    "shared-mime-info",
]
triggers = [
    "/usr/lib/gtk-3.0/3.0.0/immodules",
]
pkgdesc = "GIMP Toolkit version 3"
license = "LGPL-2.1-or-later"
url = "https://gtk.org"
source = "https://download.gnome.org/sources/gtk+/3.24/gtk+-3.24.43.tar.xz"
sha256 = "7e04f0648515034b806b74ae5d774d87cffb1a2a96c468cb5be476d51bf2f3c7"
hardening = ["!int"]
# tests require a display or a full graphics stack
options = ["!check", "etcfiles"]


@subpackage("gtk+3-devel")
def _(self):
    return self.default_devel()


def post_patch(self):
    # muon rejects string values for boolean options; upstream meson accepts
    # value: 'false'/'true', so normalize them before configure
    mf = self.cwd / "meson_options.txt"
    text = mf.read_text()
    text = text.replace("value: 'false'", "value: false")
    text = text.replace("value: 'true'", "value: true")
    mf.write_text(text)


def post_install(self):
    self.install_license("COPYING")
