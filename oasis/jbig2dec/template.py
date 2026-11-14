pkgname = "jbig2dec"
pkgver = "0.19"
pkgrel = 0
# Oasis pkg/jbig2dec/src
_commit = "1c336b8ab44524dc56ea837e2211ff4207704cdd"
pkgdesc = "JBIG2 decoder library"
license = "AGPL-3.0-or-later"
url = "https://github.com/ArtifexSoftware/jbig2dec"
source = f"https://github.com/ArtifexSoftware/jbig2dec/archive/refs/tags/{pkgver}.tar.gz"
sha256 = "e81b787ad0b147a437a52d9ce7de1a8f429655e8aa030383b6b2dd8919373717"
# static-only library, as in the Oasis recipe
options = ["!lto", "!check"]

_cflags = ["-Wall", "-DHAVE_STDINT_H", "-DHAVE_GETOPT_H", "-I."]

_sources = [
    "jbig2_arith.c",
    "jbig2_arith_int.c",
    "jbig2_arith_iaid.c",
    "jbig2_huffman.c",
    "jbig2_hufftab.c",
    "jbig2_segment.c",
    "jbig2_page.c",
    "jbig2_symbol_dict.c",
    "jbig2_text.c",
    "jbig2_halftone.c",
    "jbig2_generic.c",
    "jbig2_refinement.c",
    "jbig2_mmr.c",
    "jbig2_image.c",
    "jbig2.c",
]


def build(self):
    from cbuild.util import compiler

    cc = compiler.C(self)
    self.mkdir("obj", parents=True)
    objs = []
    for src in _sources:
        obj = "obj/" + src.removesuffix(".c") + ".o"
        cc.invoke([src], obj, obj_file=True, flags=_cflags)
        objs.append(obj)
    self.do("ar", "rcs", "libjbig2dec.a", *objs)


def install(self):
    self.install_lib("libjbig2dec.a", mode=0o644)
    self.install_file("jbig2.h", "usr/include")
    self.install_license("COPYING")


@subpackage("jbig2dec-devel")
def _(self):
    return ["usr/include"]
