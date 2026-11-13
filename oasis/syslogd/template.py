pkgname = "syslogd"
pkgver = "0_git20200623"
pkgrel = 0
# Oasis pkg/syslogd/src
_commit = "4f40184d8ada98fb61d821d1a1bcf9ebd68d1f66"
pkgdesc = "System logger"
license = "ISC"
url = "https://github.com/oasislinux/syslogd"
source = f"{url}/archive/{_commit}.tar.gz"
sha256 = "29eb3dc7e8c043c991350938c8d1e177920196d681ba356da9775ed538a2d991"
# no test suite in the Oasis recipe
options = ["!check"]

_cflags = ["-std=c11", "-Wall", "-Wextra", "-Wpedantic"]


def build(self):
    from cbuild.util import compiler

    cc = compiler.C(self)
    cc.invoke(["syslogd.c"], "syslogd", flags=_cflags)


def install(self):
    self.install_bin("syslogd")
    self.install_license("LICENSE")
