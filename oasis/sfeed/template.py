pkgname = "sfeed"
pkgver = "2.4"
pkgrel = 0
makedepends = ["netbsd-curses-devel", "netbsd-curses-devel-static"]
pkgdesc = "RSS and Atom parser"
license = "ISC"
url = "https://codemadness.org/sfeed-simple-feed-parser.html"
source = f"https://codemadness.org/releases/sfeed/sfeed-{pkgver}.tar.gz"
sha256 = "f9503fe9205a8136f76a9b753c6007abad33e2a516807e416a986723db06e879"
# no test suite in the Oasis recipe
options = ["!check"]

_cflags = [
    "-std=c99",
    "-Wall",
    "-Wpedantic",
    "-D_XOPEN_SOURCE=700",
    '-DSFEED_THEME="themes/mono.h"',
]

_tools = [
    "sfeed",
    "sfeed_atom",
    "sfeed_frames",
    "sfeed_gopher",
    "sfeed_html",
    "sfeed_json",
    "sfeed_mbox",
    "sfeed_opml_import",
    "sfeed_plain",
    "sfeed_twtxt",
    "sfeed_web",
    "sfeed_xmlenc",
]

_scripts = [
    "sfeed_content",
    "sfeed_markread",
    "sfeed_opml_export",
    "sfeed_update",
]


def build(self):
    from cbuild.util import compiler

    cc = compiler.C(self)
    self.mkdir("obj", parents=True)
    objs = []
    for src in ("util.c", "xml.c"):
        obj = "obj/" + src.removesuffix(".c") + ".o"
        cc.invoke([src], obj, obj_file=True, flags=_cflags)
        objs.append(obj)
    self.do("ar", "rcs", "libutil.a", *objs)

    for tool in _tools:
        cc.invoke([f"{tool}.c", "libutil.a"], tool, flags=_cflags)

    cc.invoke(
        ["sfeed_curses.c", "libutil.a"],
        "sfeed_curses",
        flags=_cflags,
        ldflags=["/usr/lib/libcurses.a", "/usr/lib/libterminfo.a"],
    )


def install(self):
    for tool in _tools:
        self.install_bin(tool)
    for script in _scripts:
        self.install_bin(script)
    self.install_bin("sfeed_curses")

    for man in (
        *[f"{t}.1" for t in _tools],
        "sfeed_curses.1",
        *[f"{s}.1" for s in _scripts],
        "sfeedrc.5",
    ):
        self.install_man(man)

    self.install_license("LICENSE")
