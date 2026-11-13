pkgname = "pax"
pkgver = "0_git20261029"
pkgrel = 0
# Oasis pkg/pax/src
_commit = "c2a77c3ea3d60ee11373d47560a4f7c41af832a5"
pkgdesc = "POSIX archive utility"
license = "Unlicense"
url = "https://git.sr.ht/~mcf/pax"
source = f"{url}/archive/{_commit}.tar.gz"
sha256 = "45211bb95a32e1803d163bf306d1223b963896f821621d21f435eb4a780748c5"
# no test suite in the Oasis recipe
options = ["!check"]

_cflags = ["-std=c99", "-Wall", "-Wpedantic"]


def build(self):
    from cbuild.util import compiler

    cc = compiler.C(self)
    cc.invoke(["pax.c"], "pax", flags=_cflags)


def install(self):
    self.install_bin("pax")
    self.install_license("LICENSE")
