pkgname = "nsd"
pkgver = "4.3.6"
pkgrel = 0
build_style = "gnu_configure"
configure_args = ["--with-ssl=/usr"]
configure_gen = []
makedepends = ["byacc", "flex", "libevent-devel", "libevent-devel-static", "libressl-devel", "m4"]
pkgdesc = "Authoritative DNS name server"
license = "BSD-3-Clause"
url = "https://www.nlnetlabs.nl/projects/nsd"
source = f"https://www.nlnetlabs.nl/downloads/nsd/nsd-{pkgver}.tar.gz"
sha256 = "bee6c0cf5525acc41dade9ec9e29435299211b0de290059878f7e53249e75f18"
# no test suite in the Oasis recipe
options = ["etcfiles", "!check"]


def post_install(self):
    self.install_license("LICENSE")
