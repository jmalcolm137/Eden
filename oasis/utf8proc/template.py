pkgname = "utf8proc"
pkgver = "2.7.0"
pkgrel = 0
# Oasis pkg/utf8proc/src
_commit = "8ca6144c85c165987cb1c5d8395c7314e13d4cd7"
pkgdesc = "UTF-8 processing library from Oasis"
license = "MIT"
url = "https://juliastrings.github.io/utf8proc"
source = f"https://github.com/JuliaLang/utf8proc/archive/{_commit}.tar.gz"
sha256 = "b9eea86f1501a31043f1c74f9aed9cfb9caf1b25353c47fe82c389e81106d03c"
# no test suite
options = ["!check", "!lto"]


def build(self):
    from cbuild.util import compiler

    cc = compiler.C(self)
    cc.invoke(
        ["utf8proc.c"],
        "utf8proc.o",
        obj_file=True,
        flags=["-std=c99", "-Wall", "-Wpedantic"],
    )
    self.do("ar", "rcs", "libutf8proc.a", "utf8proc.o")


def install(self):
    self.install_file("libutf8proc.a", "usr/lib")
    self.install_file("utf8proc.h", "usr/include")
    self.install_license("LICENSE.md")
