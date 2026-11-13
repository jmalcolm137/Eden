pkgname = "atinout"
pkgver = "0.9.1"
pkgrel = 0
# Oasis pkg/atinout/src; SourceForge mirror on GitHub
_commit = "0ee0208c9821a7a0d1f2fb5bd91770be76699d2f"
pkgdesc = "AT command sequence runner"
license = "GPL-3.0-or-later"
url = "https://atinout.sourceforge.net"
source = f"https://github.com/beralt/atinout/archive/{_commit}.tar.gz"
sha256 = "0987674c0d493d9e2ec611465fb8c5026244565d54886eb73aa6fc1af0b31838"
# no test suite in the Oasis recipe
options = ["!check"]

_cflags = [
    "-std=c99",
    "-Wall",
    "-Wextra",
    "-Wpedantic",
    "-Wno-implicit-fallthrough",
    '-DVERSION="0.9.1"',
]


def build(self):
    from cbuild.util import compiler

    cc = compiler.C(self)
    cc.invoke(["atinout.c"], "atinout", flags=_cflags)


def install(self):
    self.install_bin("atinout")
    self.install_license("gplv3.txt")
