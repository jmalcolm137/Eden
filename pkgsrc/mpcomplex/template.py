pkgname = "mpcomplex"
pkgver = "1.3.1"
pkgrel = 0
build_style = "gnu_configure"
configure_gen = []
hostmakedepends = ["pkgconf"]
makedepends = ["gmp-devel", "mpfr-devel"]
pkgdesc = "Multiprecision complex arithmetic library"
license = "LGPL-3.0-or-later"
url = "https://www.multiprecision.org/mpc"
source = f"https://ftp.gnu.org/gnu/mpc/mpc-{pkgver}.tar.gz"
sha256 = "ab642492f5cf882b74aa0cb730cd410a81edcdbec895183ce930e706c1c759b8"
# no test suite
options = ["!check"]


@subpackage("mpcomplex-devel")
def _(self):
    self.depends += makedepends

    return self.default_devel(extra=["usr/share"])
