pkgname = "pdpmake"
pkgver = "2.0.4"
pkgrel = 0
# Oasis pkg/pdpmake/src
_commit = "0faaf258c9b3eaa9f5e4f6842e2484cbea6f23f8"
pkgdesc = "Public domain POSIX make"
license = "Unlicense"
url = "https://github.com/rmyorston/pdpmake"
source = f"{url}/archive/{_commit}.tar.gz"
sha256 = "779fe0750e11685565de641dbabb5431330acbba182345a363f494034466dbc2"
# no test suite in the Oasis recipe
options = ["!check"]

_cflags = ["-std=c99", "-Wpedantic", "-Wall"]


def build(self):
    from cbuild.util import compiler

    cc = compiler.C(self)
    cc.invoke(
        [
            "check.c",
            "input.c",
            "macro.c",
            "main.c",
            "make.c",
            "modtime.c",
            "rules.c",
            "target.c",
            "utils.c",
        ],
        "pdpmake",
        flags=_cflags,
    )


def install(self):
    self.install_bin("pdpmake")
    self.install_man("pdpmake.1")
    self.install_license("LICENSE")
