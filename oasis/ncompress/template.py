pkgname = "ncompress"
pkgver = "5.0"
pkgrel = 1
# Oasis pkg/ncompress/src
_commit = "e77a84ca5a69f01ccfe149e48d10ac563e6c375b"
pkgdesc = "Fast LZW compression and decompression"
license = "Unlicense"
url = "https://github.com/vapier/ncompress"
source = f"{url}/archive/{_commit}.tar.gz"
sha256 = "0905f89daa94853c4c75bfe7fc9b7636a70afd7d84abdd10ee944349de3117b1"
# no test suite in the Oasis recipe
options = ["!check"]

_cflags = [
    "-std=c99",
    "-Wall",
    "-Wpedantic",
    "-D_POSIX_C_SOURCE=200809L",
    "-DUTIME_H",
    "-DLSTAT",
    "-DUSERMEM=800000",
]


def build(self):
    from cbuild.util import compiler

    cc = compiler.C(self)
    cc.invoke(["compress.c"], "lzw", flags=_cflags)


def install(self):
    self.install_bin("lzw")
    self.install_license("UNLICENSE")
