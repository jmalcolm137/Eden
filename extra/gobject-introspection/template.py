pkgname = "gobject-introspection"
pkgver = "1.86.0"
pkgrel = 1
build_style = "meson"
configure_args = [
    "-Dcairo=disabled",
    "-Ddoctool=disabled",
    "-Dgtk_doc=false",
    "-Dtests=false",
    "-Dbuild_introspection_data=false",
]
meson_impl = "meson"
hostmakedepends = [
    "bison",
    "flex",
    "meson-real",
    "pkgconf",
    "python",
    "python-mako",
    "python-markdown",
    "python-setuptools",
    "samurai",
]
makedepends = ["glib-devel", "libffi8-devel", "python-devel"]
depends = ["python", "python-mako", "python-markdown", "python-setuptools"]
pkgdesc = "Introspection system for GObject-based libraries"
license = "GPL-2.0-or-later AND LGPL-2.1-or-later"
url = "https://wiki.gnome.org/Projects/GObjectIntrospection"
source = "https://download.gnome.org/sources/gobject-introspection/1.86/gobject-introspection-1.86.0.tar.xz"
sha256 = "920d1a3fcedeadc32acff95c2e203b319039dd4b4a08dd1a2dfd283d19c0b9ae"
hardening = ["!int"]
# tests are not needed and LTO crashes the scanner
options = ["!check", "!lto"]


def post_install(self):
    from cbuild.util import python

    for f in (self.destdir / "usr/lib/gobject-introspection/giscanner").glob(
        "_giscanner*.so"
    ):
        self.mv(f, f.with_name("_giscanner.so"))
    python.precompile(self, "usr/lib/gobject-introspection/giscanner")


@subpackage("gobject-introspection-libs")
def _(self):
    return self.default_libs()


@subpackage("gobject-introspection-devel")
def _(self):
    self.depends += ["cairo-devel", "libffi8-devel"]
    return self.default_devel()
