pkgname = "libressl"
pkgver = "4.3.1"
pkgrel = 0
build_style = "gnu_configure"
configure_args = ["--disable-tests"]
configure_gen = []
hostmakedepends = ["perl"]
pkgdesc = "OpenBSD TLS and cryptography library"
license = "OpenSSL"
url = "https://www.libressl.org"
source = f"https://cdn.openbsd.org/pub/OpenBSD/LibreSSL/libressl-{pkgver}.tar.gz"
sha256 = "c2db42ace14e7d5419826fab35a742ec6e4d12725a051a51d0cea3c10ba0fa50"
# no test suite in the Oasis recipe
options = ["etcfiles", "!check"]


@subpackage("libressl-devel")
def _(self):
    return self.default_devel()
