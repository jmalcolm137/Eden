pkgname = "less"
pkgver = "643"
pkgrel = 0
makedepends = ["netbsd-curses-devel", "netbsd-curses-devel-static"]
pkgdesc = "Terminal pager"
license = "GPL-3.0-or-later"
url = "https://www.greenwoodsoftware.com/less"
source = f"{url}/less-{pkgver}.tar.gz"
sha256 = "2911b5432c836fa084c8a2e68f6cd6312372c026a58faaa98862731c8b6052e8"
# no test suite in the Oasis recipe
options = ["!check"]

_cflags = [
    "-std=c99",
    "-Wall",
    "-Wpedantic",
    "-Wno-maybe-uninitialized",
    "-D_XOPEN_SOURCE=700",
    "-I.",
]

_less_sources = [
    "main.c",
    "screen.c",
    "brac.c",
    "ch.c",
    "charset.c",
    "cmdbuf.c",
    "command.c",
    "cvt.c",
    "decode.c",
    "edit.c",
    "filename.c",
    "forwback.c",
    "help.c",
    "ifile.c",
    "input.c",
    "jump.c",
    "line.c",
    "linenum.c",
    "lsystem.c",
    "mark.c",
    "optfunc.c",
    "option.c",
    "opttbl.c",
    "os.c",
    "output.c",
    "pattern.c",
    "position.c",
    "prompt.c",
    "search.c",
    "signal.c",
    "tags.c",
    "ttyin.c",
]


def pre_build(self):
    self.cp(self.files_path / "defines.h", "defines.h")


def build(self):
    from cbuild.util import compiler

    cc = compiler.C(self)
    self.mkdir("obj", parents=True)
    objs = []
    for src in ("lesskey_parse.c", "version.c", "xbuf.c"):
        obj = "obj/" + src.removesuffix(".c") + ".o"
        cc.invoke([src], obj, obj_file=True, flags=_cflags)
        objs.append(obj)

    cc.invoke(
        _less_sources + ["obj/version.o", "obj/xbuf.o", "obj/lesskey_parse.o"],
        "less",
        flags=_cflags,
        ldflags=["/usr/lib/libcurses.a", "/usr/lib/libterminfo.a"],
    )
    cc.invoke(["lessecho.c", "obj/version.o"], "lessecho", flags=_cflags)
    cc.invoke(
        ["lesskey.c", "obj/lesskey_parse.o", "obj/xbuf.o", "obj/version.o"],
        "lesskey",
        flags=_cflags,
    )


def install(self):
    self.install_bin("less")
    self.install_bin("lessecho")
    self.install_bin("lesskey")
    self.install_link("usr/bin/more", "less")
    self.install_man("less.nro", name="less", cat=1)
    self.install_man("lessecho.nro", name="lessecho", cat=1)
    self.install_man("lesskey.nro", name="lesskey", cat=1)
    self.install_license("COPYING")
