pkgname = "nettle"
pkgver = "4.0"
pkgrel = 1
build_style = "gnu_configure"
configure_args = [
    "--disable-documentation",
    "--disable-openssl",
]
configure_gen = []
hostmakedepends = ["m4", "pkgconf"]
makedepends = ["gmp-devel"]
pkgdesc = "Low-level cryptographic library"
license = "LGPL-3.0-or-later OR GPL-2.0-or-later"
url = "https://www.lysator.liu.se/~nisse/nettle"
source = f"https://www.lysator.liu.se/~nisse/archive/nettle-{pkgver}.tar.gz"
sha256 = "3addbc00da01846b232fb3bc453538ea5468da43033f21bb345cb1e9073f5094"
# tests need the full upstream corpus
options = ["!check"]


@subpackage("nettle-devel")
def _(self):
    return self.default_devel()


@subpackage("nettle-progs")
def _(self):
    return self.default_progs()


def post_install(self):
    self.install_license("COPYINGv3")
