pkgname = "libxkbcommon"
pkgver = "1.3.1"
pkgrel = 0
# Oasis pkg/libxkbcommon/src
_commit = "88222c8d40543c29af781f7d7e25d202ff40e4b7"
pkgdesc = "Keyboard description library from Oasis"
license = "MIT"
url = "https://xkbcommon.org"
source = f"https://github.com/xkbcommon/libxkbcommon/archive/{_commit}.tar.gz"
sha256 = "c411fbb494e7febad4ad6237065181b8de52619b4d044e583df1ac54c391eea4"
# no test suite
options = ["!check", "!lto"]

_sources = [
    "src/compose/parser.c",
    "src/compose/paths.c",
    "src/compose/state.c",
    "src/compose/table.c",
    "src/xkbcomp/action.c",
    "src/xkbcomp/ast-build.c",
    "src/xkbcomp/compat.c",
    "src/xkbcomp/expr.c",
    "src/xkbcomp/include.c",
    "src/xkbcomp/keycodes.c",
    "src/xkbcomp/keymap.c",
    "src/xkbcomp/keymap-dump.c",
    "src/xkbcomp/keywords.c",
    "src/xkbcomp/parser.c",
    "src/xkbcomp/rules.c",
    "src/xkbcomp/scanner.c",
    "src/xkbcomp/symbols.c",
    "src/xkbcomp/types.c",
    "src/xkbcomp/vmod.c",
    "src/xkbcomp/xkbcomp.c",
    "src/atom.c",
    "src/context.c",
    "src/context-priv.c",
    "src/keysym.c",
    "src/keysym-utf.c",
    "src/keymap.c",
    "src/keymap-priv.c",
    "src/state.c",
    "src/text.c",
    "src/utf8.c",
    "src/utils.c",
]


def pre_build(self):
    self.cp(self.files_path / "config.h", "config.h")
    self.cp(self.files_path / "xkbcommon.patch", "xkbcommon.patch")
    self.do("patch", "-p1", "-i", "xkbcommon.patch")


def build(self):
    from cbuild.util import compiler

    cc = compiler.C(self)
    objs = []
    flags = ["-I.", "-Iinclude", "-Isrc"]
    self.mkdir("obj", parents=True)

    for src in _sources:
        obj = "obj/" + src.replace("/", "_").removesuffix(".c") + ".o"
        cc.invoke([src], obj, obj_file=True, flags=flags)
        objs.append(obj)

    self.do("ar", "rcs", "libxkbcommon.a", *objs)


def install(self):
    self.install_file("libxkbcommon.a", "usr/lib")
    for src in sorted((self.cwd / "include/xkbcommon").glob("*.h")):
        self.install_file(f"include/xkbcommon/{src.name}", "usr/include/xkbcommon")
    self.install_file(self.files_path / "xkbcommon.pc", "usr/lib/pkgconfig")
    self.install_license("LICENSE")
