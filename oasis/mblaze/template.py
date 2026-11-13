pkgname = "mblaze"
pkgver = "1.4"
pkgrel = 0
# Oasis pkg/mblaze/src
_commit = "7b039011ef688e030ffe9eebe831d1ac8619072b"
pkgdesc = "Mail utilities"
license = "CC0-1.0"
url = "https://github.com/leahneukirchen/mblaze"
source = f"{url}/archive/{_commit}.tar.gz"
sha256 = "53316c29a7b3d59d4db818bb667e557c412def8b0b007e21736f836c5486b05d"
# no test suite in the Oasis recipe
options = ["!check"]

_cflags = [
    "-std=c99",
    "-Wall",
    "-Wextra",
    "-Wpedantic",
    "-Wno-switch",
    "-D_XOPEN_SOURCE=700",
]

_lib_sources = [
    "blaze822.c",
    "filter.c",
    "mymemmem.c",
    "mystrverscmp.c",
    "mytimegm.c",
    "pipeto.c",
    "rfc2045.c",
    "rfc2047.c",
    "rfc2231.c",
    "safe_u8putstr.c",
    "seq.c",
    "slurp.c",
    "squeeze_slash.c",
]

_tools = [
    "maddr",
    "magrep",
    "mdate",
    "mdeliver",
    "mdirs",
    "mexport",
    "mflag",
    "mflow",
    "mgenmid",
    "mhdr",
    "minc",
    "mlist",
    "mmime",
    "mpick",
    "mscan",
    "msed",
    "mseq",
    "mshow",
    "msort",
    "mthread",
]

_scripts = ["mcolor", "mcom", "mless", "mmkdir", "mquote"]


def build(self):
    from cbuild.util import compiler

    cc = compiler.C(self)
    self.mkdir("obj", parents=True)
    objs = []
    for src in _lib_sources:
        obj = "obj/" + src.removesuffix(".c") + ".o"
        cc.invoke([src], obj, obj_file=True, flags=_cflags)
        objs.append(obj)
    self.do("ar", "rcs", "libcommon.a", *objs)

    for tool in _tools:
        cc.invoke([f"{tool}.c", "libcommon.a"], tool, flags=_cflags)


def install(self):
    for tool in _tools:
        self.install_bin(tool)
    for script in _scripts:
        self.install_bin(script)

    self.install_link("usr/bin/mbnc", "mcom")
    self.install_link("usr/bin/mfwd", "mcom")
    self.install_link("usr/bin/mrep", "mcom")

    version = (self.cwd / "VERSION").read_text().strip()
    self.install_dir("usr/bin")
    museragent = self.destdir / "usr/bin/museragent"
    museragent.write_text(
        "#!/bin/sh\nexec printf \"User-Agent: mblaze/%s\\n\" \"%s\"\n"
        % (version, version)
    )
    museragent.chmod(0o755)

    for man in sorted((self.cwd / "man").glob("*.1")):
        self.install_man(man)
    for man in sorted((self.cwd / "man").glob("*.5")):
        self.install_man(man)
    for man in sorted((self.cwd / "man").glob("*.7")):
        self.install_man(man)

    self.install_license("COPYING")
