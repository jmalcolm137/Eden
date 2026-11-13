pkgname = "vis"
pkgver = "0.9"
pkgrel = 1
# Oasis pkg/vis/src
_commit = "50a7673370fa037960e9d2c3a8d6aed1bb9c39c4"
archs = ["aarch64", "riscv64", "x86_64"]
makedepends = [
    "libtermkey",
    "lpeg",
    "lua",
    "netbsd-curses-devel",
    "netbsd-curses-devel-static",
]
pkgdesc = "Modal text editor from Oasis"
license = "ISC AND MIT AND CC0-1.0"
url = "https://github.com/martanne/vis"
source = f"{url}/archive/{_commit}.tar.gz"
sha256 = "7f48aefc94a1402369f23518beeb21264ce9bb5868242670a0865828fa496c57"
# upstream has no test suite
options = ["!check"]

_sources = [
    "array.c",
    "buffer.c",
    "libutf.c",
    "main.c",
    "map.c",
    "sam.c",
    "text.c",
    "text-common.c",
    "text-io.c",
    "text-iterator.c",
    "text-motions.c",
    "text-objects.c",
    "text-util.c",
    "ui-terminal.c",
    "view.c",
    "vis.c",
    "vis-lua.c",
    "vis-marks.c",
    "vis-modes.c",
    "vis-motions.c",
    "vis-operators.c",
    "vis-prompt.c",
    "vis-registers.c",
    "vis-text-objects.c",
    "vis-subprocess.c",
    "text-regex.c",
]

_cflags = [
    "-std=c99",
    "-DCONFIG_HELP=1",
    "-DCONFIG_CURSES=1",
    "-DCONFIG_LUA=1",
    "-DCONFIG_LPEG=1",
    "-DCONFIG_TRE=0",
    "-DCONFIG_SELINUX=0",
    "-DCONFIG_ACL=0",
    "-DHAVE_MEMRCHR=1",
    "-DLUA_COMPAT_APIINTCASTS",
    "-D_XOPEN_SOURCE=700",
    '-DVERSION="v0.9"',
    '-DVIS_PATH="/usr/share/vis"',
    "-DNDEBUG",
    "-I.",
]


def pre_build(self):
    self.cp("config.def.h", "config.h")


def build(self):
    from cbuild.util import compiler

    cc = compiler.C(self)
    objs = []

    self.mkdir("obj", parents=True)
    for src in _sources:
        obj = "obj/" + src.removesuffix(".c") + ".o"
        cc.invoke([src], obj, obj_file=True, flags=_cflags)
        objs.append(obj)

    cc.invoke(
        objs,
        "vis",
        ldflags=[
            "/usr/lib/libtermkey.a",
            "/usr/lib/liblpeg.a",
            "/usr/lib/liblua.a",
            "/usr/lib/libcurses.a",
            "/usr/lib/libterminfo.a",
            "-lm",
            "-ldl",
        ],
    )
    cc.invoke(["vis-menu.c"], "vis-menu", flags=_cflags)
    cc.invoke(["vis-digraph.c"], "vis-digraph", flags=_cflags)


def install(self):
    self.install_bin("vis")
    self.install_bin("vis-menu")
    self.install_bin("vis-digraph")
    self.install_file("vis-open", "usr/bin", mode=0o755)

    for man in ["vis.1", "vis-digraph.1", "vis-menu.1", "vis-open.1"]:
        text = (self.cwd / "man" / man).read_text()
        (self.cwd / man).write_text(text.replace("VERSION", "v0.9"))
        self.install_man(man)

    for src in sorted((self.cwd / "lua").rglob("*.lua")):
        # the Oasis file list only includes regular files; the aliases are
        # installed as symlinks below
        if src.is_symlink():
            continue
        rel = src.relative_to(self.cwd / "lua")
        dest = "usr/share/vis"
        if str(rel.parent) != ".":
            dest += f"/{rel.parent}"
        self.install_file(f"lua/{rel}", dest)

    self.install_link("usr/share/vis/lexer.lua", "lexers/lexer.lua")
    self.install_link("usr/share/vis/themes/default.lua", "base-16.lua")

    self.install_license("LICENSE")
