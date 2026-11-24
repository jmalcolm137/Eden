pkgname = "gnu-m4"
pkgver = "1.4.20"
pkgrel = 2
build_style = "gnu_configure"
# the OpenBSD userland already provides /usr/bin/m4; install GNU m4 as gm4
configure_args = ["--program-prefix=g"]
configure_gen = []
pkgdesc = "GNU macro processor"
license = "GPL-3.0-or-later"
url = "https://www.gnu.org/software/m4"
source = f"$(GNU_SITE)/m4/m4-{pkgver}.tar.xz"
sha256 = "e236ea3a1ccf5f6c270b1c4bb60726f371fa49459a8eaaebc90b216b328daf2b"
# long autotest suite, not needed for a build tool
options = ["!check", "bootstrap"]


def post_install(self):
    # the /usr/gnubin/m4 name is provided by gnu-compat
    self.install_license("COPYING")
