pkgname = "kbd"
pkgver = "2.4.0"
pkgrel = 0
makedepends = ["linux-headers"]
pkgdesc = "Keyboard and console utilities"
license = "GPL-2.0-or-later"
url = "https://www.kernel.org/pub/linux/utils/kbd"
source = f"{url}/kbd-{pkgver}.tar.gz"
sha256 = "cd7852ef59fd01d1b125a5f7241b39fd2b58ca8097b69766eae478e47cc83c3b"
# no test suite in the Oasis recipe
options = ["!check"]

_cflags = [
    "-Wall",
    "-Wno-stringop-truncation",
    '-DDATADIR="/usr/share/kbd"',
    "-I.",
    "-Isrc",
    "-Isrc/libcommon",
    "-Isrc/libkbdfile",
    "-Isrc/libkeymap",
    "-Isrc/libkeymap/keymap",
    "-Isrc/libkfont",
]

_libs = [
    ("libcommon.a", ["src/libcommon/getfd.c", "src/libcommon/error.c", "src/libcommon/version.c"]),
    ("libkbdfile.a", ["src/libkbdfile/init.c", "src/libkbdfile/kbdfile.c"]),
    ("libkeymap.a", [
        "src/libkeymap/analyze.c", "src/libkeymap/array.c", "src/libkeymap/common.c",
        "src/libkeymap/diacr.c", "src/libkeymap/dump.c", "src/libkeymap/func.c",
        "src/libkeymap/kernel.c", "src/libkeymap/kmap.c", "src/libkeymap/ksyms.c",
        "src/libkeymap/loadkeys.c", "src/libkeymap/modifiers.c", "src/libkeymap/parser.c",
        "src/libkeymap/summary.c",
    ]),
    ("libkfont.a", [
        "src/libkfont/psffontop.c", "src/libkfont/psfxtable.c", "src/libkfont/context.c",
        "src/libkfont/unicode.c", "src/libkfont/utf8.c", "src/libkfont/kdmapop.c",
        "src/libkfont/loadunimap.c", "src/libkfont/mapscrn.c", "src/libkfont/setfont.c",
        "src/libkfont/kdfontop.c",
    ]),
]

_tools = [
    ("deallocvt", "1", False),
    ("dumpkeys", "1", True),
    ("fgconsole", "1", False),
    ("getkeycodes", "8", False),
    ("kbd_mode", "1", False),
    ("kbdinfo", None, False),
    ("loadkeys", "1", True),
    ("openvt", "1", False),
    ("psfxtable", "1", False),
    ("setfont", "8", True),
    ("setkeycodes", "8", False),
    ("setvtrgb", "8", False),
    ("showconsolefont", "8", False),
    ("showkey", "1", False),
]


def pre_build(self):
    self.cp(self.files_path / "config.h", "config.h")


def build(self):
    from cbuild.util import compiler

    cc = compiler.C(self)
    self.mkdir("obj", parents=True)
    for lib, sources in _libs:
        objs = []
        for src in sources:
            obj = "obj/" + src.replace("/", "_").removesuffix(".c") + ".o"
            cc.invoke([src], obj, obj_file=True, flags=_cflags)
            objs.append(obj)
        self.do("ar", "rcs", lib, *objs)

    libs = [lib for lib, _ in _libs]
    for name, _sect, _subst in _tools:
        cc.invoke([f"src/{name}.c", *libs], name, flags=_cflags)


def install(self):
    for name, sect, subst in _tools:
        self.install_bin(name)
        if not sect:
            continue
        man = f"docs/man/man{sect}/{name}.{sect}"
        if subst:
            text = (self.cwd / f"{man}.in").read_text()
            (self.cwd / f"{name}.{sect}").write_text(
                text.replace("@DATADIR@", "/share/kbd")
            )
            self.install_man(f"{name}.{sect}")
        else:
            self.install_man(man)

    for line in (self.files_path / "keymaps.txt").read_text().splitlines():
        line = line.strip()
        if not line or line.startswith("#"):
            continue
        dest = "usr/share/kbd/keymaps/" + line.rsplit("/", 1)[0]
        self.install_file(f"data/keymaps/{line}", dest)
    self.install_link("usr/share/kbd/keymaps/ppc", "mac")
    self.install_license("COPYING")
