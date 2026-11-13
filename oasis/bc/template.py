pkgname = "bc"
pkgver = "1.08.2"
pkgrel = 0
pkgdesc = "Arbitrary precision calculator language"
license = "GPL-3.0-or-later"
url = "https://www.gnu.org/software/bc"
source = f"https://ftp.gnu.org/gnu/bc/bc-{pkgver}.tar.gz"
sha256 = "ae470fec429775653e042015edc928d07c8c3b2fc59765172a330d3d87785f86"
# no test suite in the Oasis recipe
options = ["!check"]

_cflags = [
    "-std=c99",
    "-Wall",
    "-Wpedantic",
    "-D_POSIX_C_SOURCE=200809L",
    "-I.",
    "-Ih",
]


def pre_build(self):
    self.cp(self.files_path / "config.h", "config.h")
    self.mkdir("build", parents=True)


def build(self):
    from cbuild.util import compiler

    cc = compiler.C(self)
    cc.invoke(
        [
            "bc/main.c",
            "bc/bc.c",
            "bc/scan.c",
            "bc/execute.c",
            "bc/load.c",
            "bc/storage.c",
            "bc/util.c",
            "bc/global.c",
            "bc/warranty.c",
            "lib/number.c",
        ],
        "build/bc",
        flags=_cflags,
    )


def install(self):
    self.install_bin("build/bc", name="bc")
    self.install_man("doc/bc.1")
    self.install_license("COPYING")
