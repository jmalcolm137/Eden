pkgname = "hyx"
pkgver = "2026.01.11"
pkgrel = 0
pkgdesc = "Minimalistic hexadecimal editor"
license = "MIT"
url = "https://yx7.cc/code/hyx"
source = f"{url}/hyx-{pkgver}.tar.xz"
sha256 = "550863c9e6a2c0e2618c16a562c8ee995e88c1d30e62abfdf4ecb819b3c4df54"
# no test suite in the Oasis recipe
options = ["!check"]

_cflags = [
    "-std=c99",
    "-Wall",
    "-Wextra",
    "-Wpedantic",
    "-DNDEBUG",
]


def build(self):
    from cbuild.util import compiler

    cc = compiler.C(self)
    cc.invoke(
        [
            "blob.c",
            "common.c",
            "history.c",
            "hyx.c",
            "input.c",
            "term.c",
            "view.c",
        ],
        "hyx",
        flags=_cflags,
    )


def install(self):
    self.install_bin("hyx")
    self.install_license("license.txt")
