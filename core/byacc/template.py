pkgname = "byacc"
pkgver = "20260126"
pkgrel = 0
# Oasis pkg/byacc
pkgdesc = "Berkeley yacc, a LALR(1) parser generator"
license = "custom:byacc"
url = "https://invisible-island.net/byacc"
source = f"https://invisible-mirror.net/archives/byacc/byacc-{pkgver}.tgz"
sha256 = "b618c5fb44c2f5f048843db90f7d1b24f78f47b07913c8c7ba8c942d3eb24b00"
# no test suite in the bootstrap environment
options = ["!check"]

_sources = [
    "closure.c",
    "error.c",
    "graph.c",
    "lalr.c",
    "lr0.c",
    "main.c",
    "mkpar.c",
    "mstring.c",
    "output.c",
    "reader.c",
    "yaccpar.c",
    "symtab.c",
    "verbose.c",
    "warshall.c",
]


def pre_build(self):
    self.cp(self.files_path / "config.h", "config.h")


def build(self):
    from cbuild.util import compiler

    cc = compiler.C(self)
    objs = []
    flags = [
        "-Wall",
        "-Wpedantic",
        "-DHAVE_CONFIG_H",
        "-DYYPATCH=20260126",
        "-I.",
    ]
    self.mkdir("obj", parents=True)

    for src in _sources:
        obj = "obj/" + src.removesuffix(".c") + ".o"
        cc.invoke([src], obj, obj_file=True, flags=flags)
        objs.append(obj)

    cc.invoke(objs, "byacc")


def install(self):
    self.install_bin("byacc")
    self.install_link("usr/bin/yacc", "byacc")
    self.install_file("yacc.1", "usr/share/man/man1", name="byacc.1")
    self.install_link("usr/share/man/man1/yacc.1", "byacc.1")
    self.install_license("LICENSE")
