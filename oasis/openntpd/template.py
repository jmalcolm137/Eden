pkgname = "openntpd"
pkgver = "6.8_p1"
pkgrel = 0
build_style = "gnu_configure"
configure_args = ["--with-privsep-user=root"]
configure_gen = []
makedepends = ["linux-headers"]
pkgdesc = "OpenBSD NTP daemon"
license = "ISC"
url = "https://www.openntpd.org"
source = f"https://cdn.openbsd.org/pub/OpenBSD/OpenNTPD/openntpd-{pkgver.replace('_', '')}.tar.gz"
sha256 = "8582db838a399153d4a17f2a76518b638cc3020f58028575bf54127518f55a46"
# no test suite in the Oasis recipe
options = ["etcfiles", "hardlinks", "!check"]


def post_install(self):
    self.install_license("COPYING")
