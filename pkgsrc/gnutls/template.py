pkgname = "gnutls"
pkgver = "3.8.13"
pkgrel = 1
build_style = "gnu_configure"
configure_args = [
    "--disable-doc",
    "--disable-full-test-suite",
    "--disable-guile",
    "--disable-libdane",
    "--disable-tests",
    "--disable-tools" ,
    "--without-brotli",
    "--without-idn",
    "--without-p11-kit",
    "--without-tpm",
    "--without-tpm2",
    "--without-zstd",
    "--with-included-unistring",
]
configure_gen = []
hostmakedepends = ["gettext", "libtool", "pkgconf"]
makedepends = [
    "gmp-devel",
    "libtasn1-devel",
    "linux-headers",
    "nettle-devel",
    "zlib-static",
]
pkgdesc = "GNU TLS library"
license = "LGPL-2.1-or-later"
url = "https://www.gnutls.org"
source = f"https://www.gnupg.org/ftp/gcrypt/gnutls/v{pkgver[:3]}/gnutls-{pkgver}.tar.xz"
sha256 = "ffed8ec1bf09c2426d4f14aae377de4753b53e537d685e604e99a8b16ca9c97e"
# tests need the full upstream corpus and network
options = ["!check"]


@subpackage("gnutls-devel")
def _(self):
    return self.default_devel()


def post_install(self):
    self.install_license("COPYING")
