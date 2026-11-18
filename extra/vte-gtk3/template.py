pkgname = "vte-gtk3"
pkgver = "0.80.5"
pkgrel = 0
build_style = "meson"
configure_args = [
    "-Da11y=true",
    "-Ddbg=false",
    "-Ddocs=false",
    "-Dfribidi=true",
    "-Dgir=false",
    "-Dglade=false",
    "-Dgnutls=false",
    "-Dgtk3=true",
    "-Dgtk4=false",
    "-Dicu=false",
    "-D_systemd=false",
    "-Dvapi=false",
]
meson_impl = "meson"
hostmakedepends = [
    "gettext",
    "meson-real",
    "pkgconf",
    "python",
    "samurai",
]
makedepends = [
    "cairo-devel",
    "fast_float",
    "fribidi-devel",
    "glib-devel",
    "gtk+3-devel",
    "linux-headers",
    "lz4-devel",
    "pango-devel",
    "pcre2-devel",
]
pkgdesc = "Terminal emulator widget for GTK+ 3"
license = "LGPL-3.0-or-later"
url = "https://wiki.gnome.org/Apps/Terminal/VTE"
source = f"https://download.gnome.org/sources/vte/0.80/vte-{pkgver}.tar.xz"
sha256 = "58a4e00ab5d4a95b4be4dc57b48308deafd72d6839dbbd076648fa353321cc41"
# tests need a working terminal and a display
options = ["!check", "!lto", "etcfiles"]


@subpackage("vte-gtk3-devel")
def _(self):
    return self.default_devel()


def post_install(self):
    self.install_license("COPYING.LGPL3")


def post_patch(self):
    # core lz4 ships a pc file with prefix=/usr/local; use the linker directly
    p = self.cwd / "meson.build"
    p.write_text(
        p.read_text().replace(
            "dependency('liblz4', version: '>=' + liblz4_req_version)",
            "cc.find_library('lz4', required: true)",
        )
    )
    # W_EXITCODE is a glibc extension; musl provides only the W* macros
    p = self.cwd / "src/widget.cc"
    p.write_text(
        p.read_text().replace(
            "W_EXITCODE(0, SIGKILL)", "((0 << 8) | (SIGKILL & 0x7f))"
        )
    )
