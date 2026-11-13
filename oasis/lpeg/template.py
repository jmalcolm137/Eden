pkgname = "lpeg"
pkgver = "1.1.0"
pkgrel = 0
makedepends = ["lua"]
pkgdesc = "Parsing Expression Grammars for Lua"
license = "MIT"
url = "https://www.inf.puc-rio.br/~roberto/lpeg"
source = f"{url}/lpeg-{pkgver}.tar.gz"
sha256 = "4b155d67d2246c1ffa7ad7bc466c1ea899bbc40fef0257cc9c03cecbaed4352a"
tool_flags = {"CFLAGS": ["-fPIC"]}
# the upstream test driver needs a working Lua interpreter
# static library is installed in the main package, like Oasis does
options = ["!check", "!lto"]

_sources = [
    "lpvm.c",
    "lpcap.c",
    "lptree.c",
    "lpcode.c",
    "lpprint.c",
    "lpcset.c",
]


def build(self):
    from cbuild.util import compiler

    cc = compiler.C(self)
    objs = []

    for src in _sources:
        obj = src.removesuffix(".c") + ".o"
        cc.invoke([src], obj, obj_file=True, flags=["-I/usr/include"])
        objs.append(obj)

    self.do("ar", "rcs", "liblpeg.a", *objs)


def install(self):
    self.install_file("liblpeg.a", "usr/lib")
    self.install_file(self.files_path / "lpeg.pc", "usr/lib/pkgconfig")
    self.install_license("lpeg.html")
