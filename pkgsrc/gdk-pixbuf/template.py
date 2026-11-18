pkgname = "gdk-pixbuf"
pkgver = "2.44.8"
pkgrel = 1
build_style = "meson"
configure_args = [
    "-Dbuiltin_loaders=all",
    "-Ddefault_library=shared",
    "-Ddocumentation=false",
    "-Dgif=enabled",
    "-Dglycin=disabled",
    "-Dgtk_doc=false",
    "-Dinstalled_tests=false",
    "-Dintrospection=disabled",
    "-Djpeg=enabled",
    "-Dman=false",
    "-Dothers=disabled",
    "-Dpng=enabled",
    "-Drelocatable=false",
    "-Dtests=false",
    "-Dthumbnailer=disabled",
    "-Dtiff=disabled",
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
    "libjpeg-turbo-devel",
    "libpng-devel",
    "shared-mime-info",
]
depends = ["shared-mime-info"]
pkgdesc = "Image loading library for GTK"
license = "LGPL-2.1-or-later"
url = "https://wiki.gnome.org/Projects/GdkPixbuf"
source = "https://download.gnome.org/sources/gdk-pixbuf/2.44/gdk-pixbuf-2.44.8.tar.xz"
sha256 = "919f529512961a12e81cd4b4b466a48c3933469e7f9a310c6513cd4fb252ba3c"
hardening = ["!int"]
# tests need a display and the upstream test suite
options = ["!check", "!lto"]


def post_install(self):
    self.install_license("COPYING")


@subpackage("gdk-pixbuf-devel")
def _(self):
    return self.default_devel(extra=["usr/bin/*csource*"])


def post_patch(self):
    # all loaders are built in, so the generated loaders.cache is only used
    # by the test suite; do not run the query tool during the build
    mf = self.cwd / "gdk-pixbuf/meson.build"
    text = mf.read_text()
    old = "                                build_by_default: true)"
    if old not in text:
        self.error("unexpected loaders.cache target in meson.build")
    text = text.replace(old, "                                build_by_default: false)")
    # builtin loaders need no cache; the query tool is broken under the
    # current toolchain, so produce an empty cache instead of running it
    target = text.index("loaders_cache = custom_target")
    q = text.index("gdk_pixbuf_query_loaders", target)
    start = text.rindex("command: [\n", 0, q)
    endm = "\n                                ],"
    end = text.index(endm, q) + len(endm)
    text = text[:start] + "command: [ 'true' ]," + text[end:]
    mf.write_text(text)
