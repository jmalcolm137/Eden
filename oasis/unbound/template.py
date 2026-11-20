pkgname = "unbound"
pkgver = "1.20.0"
pkgrel = 0
build_style = "gnu_configure"
configure_args = [
    "--with-ssl=/usr",
    "--with-libevent=/usr",
    "--with-libexpat=/usr",
    "--without-pythonmodule",
    "--disable-flto",
]
configure_gen = []
makedepends = ["byacc", "expat", "flex", "libevent", "libevent-devel", "libevent-devel-static", "libressl-devel", "m4"]
pkgdesc = "Validating, recursive, caching DNS resolver"
license = "BSD-3-Clause"
url = "https://nlnetlabs.nl/projects/unbound"
source = f"https://nlnetlabs.nl/downloads/unbound/unbound-{pkgver}.tar.gz"
sha256 = "56b4ceed33639522000fd96775576ddf8782bb3617610715d7f1e777c5ec1dbf"
# no test suite in the Oasis recipe
options = ["etcfiles", "!lto", "!check", "!scanpkgconf"]


def post_install(self):
    self.install_license("LICENSE")
