pkgname = "sdhcp"
pkgver = "0_git20190717"
pkgrel = 0
# Oasis pkg/sdhcp/src
_commit = "5f9956c8706215f8b8887c0beb77ed7d1810ec7a"
pkgdesc = "Simple DHCP client"
license = "MIT"
url = "https://github.com/michaelforney/sdhcp"
source = f"{url}/archive/{_commit}.tar.gz"
sha256 = "28613e15975df7c990a19aa0d3fd506c832cc229901e81502b0ec353ef34e4f2"
# no test suite in the Oasis recipe
options = ["!check"]

_cflags = [
    "-std=c99",
    "-Wall",
    "-Wextra",
    "-Wpedantic",
    "-D_BSD_SOURCE",
]


def build(self):
    from cbuild.util import compiler

    cc = compiler.C(self)
    cc.invoke(["sdhcp.c", "util/eprintf.c"], "sdhcp", flags=_cflags)


def install(self):
    self.install_bin("sdhcp")
    self.install_man("sdhcp.1")
    self.install_license("LICENSE")
