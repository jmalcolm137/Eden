pkgname = "m4"
pkgver = "1.4.20"
pkgrel = 0
build_style = "gnu_configure"
configure_args = ["--disable-nls"]
configure_gen = []
pkgdesc = "GNU macro processor"
license = "GPL-3.0-or-later"
url = "https://www.gnu.org/software/m4"
source = f"$(GNU_SITE)/m4/m4-{pkgver}.tar.xz"
sha256 = "e236ea3a1ccf5f6c270b1c4bb60726f371fa49459a8eaaebc90b216b328daf2b"
# glibc gnulib code trips -Werror=format-security
hardening = ["!format"]
# no test suite in the bootstrap environment
options = ["!check"]


def post_install(self):
    self.install_license("COPYING")
    # pkgsrc convention: GNU m4 is also reachable as gm4
    self.install_link("usr/bin/gm4", "m4")
    self.install_link("usr/share/man/man1/gm4.1", "m4.1")
