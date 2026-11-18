pkgname = "libssh2"
pkgver = "1.11.1"
pkgrel = 1
build_style = "gnu_configure"
configure_args = [
    "--disable-examples-build",
    "--disable-static",
    "--with-crypto=openssl",
]
configure_gen = []
hostmakedepends = ["libtool", "pkgconf"]
makedepends = ["libressl-devel", "zlib-static"]
depends = ["libressl", "zlib-shared"]
pkgdesc = "Client-side C library implementing the SSH2 protocol"
license = "BSD-3-Clause"
url = "https://www.libssh2.org"
source = f"https://www.libssh2.org/download/libssh2-{pkgver}.tar.gz"
sha256 = "d9ec76cbe34db98eec3539fe2c899d26b0c837cb3eb466a56b0f109cabf658f7"
# tests need network and a live sshd
options = ["!check"]


@subpackage("libssh2-devel")
def _(self):
    return self.default_devel()


def post_install(self):
    self.install_license("COPYING")
