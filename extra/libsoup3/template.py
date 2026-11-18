pkgname = "libsoup3"
pkgver = "3.6.6"
pkgrel = 0
build_style = "meson"
configure_args = [
    "-Dbrotli=enabled",
    "-Ddocs=disabled",
    "-Dgssapi=disabled",
    "-Dintrospection=disabled",
    "-Dntlm=disabled",
    "-Dtests=false",
    "-Dtls_check=false",
    "-Dvapi=disabled",
]
hostmakedepends = [
    "gettext",
    "meson-real",
    "pkgconf",
    "python",
    "samurai",
]
makedepends = [
    "brotli-devel",
    "glib-devel",
    "libpsl-devel",
    "nghttp2-devel",
    "sqlite-devel",
    "zlib-static",
]
pkgdesc = "HTTP client/server library for GNOME"
license = "LGPL-2.0-or-later"
url = "https://wiki.gnome.org/Projects/libsoup"
source = f"https://download.gnome.org/sources/libsoup/3.6/libsoup-{pkgver}.tar.xz"
sha256 = "51ed0ae06f9d5a40f401ff459e2e5f652f9a510b7730e1359ee66d14d4872740"
# tests need network access and a session bus
options = ["!check"]


@subpackage("libsoup3-devel")
def _(self):
    return self.default_devel()


def post_install(self):
    self.install_license("COPYING")
