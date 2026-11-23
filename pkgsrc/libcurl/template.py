pkgname = "libcurl"
pkgver = "8.23.0"
pkgrel = 1
build_style = "gnu_configure"
configure_args = [
    "--disable-ldap",
    "--disable-ldaps",
    "--disable-manual",
    "--disable-static",
    "--with-brotli",
    "--with-gnutls",
    "--with-libpsl",
    "--with-nghttp2",
    "--without-libssh2",
    "--without-zstd",
]
configure_gen = []
hostmakedepends = ["libtool", "pkgconf"]
makedepends = [
    "brotli-devel",
    "gnutls-devel",
    "libpsl-devel",
    "nghttp2-devel",
    "zlib",
]
depends = ["gnutls", "zlib-shared"]
pkgdesc = "Command line tool and library for URL transfers"
license = "curl"
url = "https://curl.se"
source = f"https://curl.se/download/curl-{pkgver}.tar.xz"
sha256 = "8dadd7d2536a314f982ad05a651b713f426bf7d02cc2c76cffb9796f2218e6c5"
# tests need network access
options = ["!check"]


@subpackage("libcurl-devel")
def _(self):
    return self.default_devel()


def post_install(self):
    # core provides the curl command; avoid a duplicate provider
    self.uninstall("usr/bin/curl", missing_ok=True)
    self.uninstall("usr/bin/curl-config", missing_ok=True)
    self.uninstall("usr/share/man/man1/curl.1", missing_ok=True)
    self.install_license("COPYING")
