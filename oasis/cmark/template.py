pkgname = "cmark"
pkgver = "0.31.2"
pkgrel = 0
# Oasis pkg/cmark/src
_commit = "eec0eeba6d31189fd828314576494566d539b1e3"
pkgdesc = "CommonMark parsing and rendering library and program"
license = "BSD-2-Clause"
url = "https://commonmark.org"
source = f"https://github.com/commonmark/cmark/archive/{_commit}.tar.gz"
sha256 = "8aa5b3f8f4ceea72ff11e9383f06097026e5201756c9297f90d41423b0c7fea6"
# no test suite in the Oasis recipe
options = ["!check"]

_cflags = ["-std=c99", "-Wall", "-Wpedantic", "-I.", "-Isrc"]

_lib_sources = [
    "blocks.c",
    "buffer.c",
    "cmark.c",
    "cmark_ctype.c",
    "commonmark.c",
    "houdini_href_e.c",
    "houdini_html_e.c",
    "houdini_html_u.c",
    "html.c",
    "inlines.c",
    "iterator.c",
    "latex.c",
    "man.c",
    "node.c",
    "references.c",
    "render.c",
    "scanners.c",
    "utf8.c",
    "xml.c",
]


def pre_build(self):
    self.cp(self.files_path / "cmark_export.h", "cmark_export.h")
    self.cp(self.files_path / "cmark_version.h", "cmark_version.h")


def build(self):
    from cbuild.util import compiler

    cc = compiler.C(self)
    self.mkdir("obj", parents=True)
    objs = []
    for src in _lib_sources:
        obj = "obj/" + src.removesuffix(".c") + ".o"
        cc.invoke([f"src/{src}"], obj, obj_file=True, flags=_cflags)
        objs.append(obj)
    self.do("ar", "rcs", "libcmark.a", *objs)
    cc.invoke(["src/main.c", "libcmark.a"], "cmark", flags=_cflags)


def install(self):
    self.install_bin("cmark")
    self.install_man("man/man1/cmark.1")
    self.install_lib("libcmark.a", mode=0o644)
    self.install_file("src/cmark.h", "usr/include")
    self.install_file(self.files_path / "cmark_export.h", "usr/include")
    self.install_file(self.files_path / "cmark_version.h", "usr/include")
    self.install_license("COPYING")


@subpackage("cmark-devel")
def _(self):
    return ["usr/include"]


@subpackage("cmark-devel-static")
def _(self):
    return ["usr/lib/*.a"]
