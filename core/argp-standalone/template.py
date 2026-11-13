pkgname = "argp-standalone"
pkgver = "1.4.1"
pkgrel = 0
pkgdesc = "Standalone argp implementation"
license = "LGPL-2.1-or-later"
url = "https://github.com/ericonr/argp-standalone"
source = f"{url}/archive/{pkgver}.tar.gz"
sha256 = "879d76374424dce051b812f16f43c6d16de8dbaddd76002f83fd1b6e57d39e0b"
# no test suite
options = ["!check", "!lto"]

_sources = [
    "argp-ba.c",
    "argp-eexst.c",
    "argp-fmtstream.c",
    "argp-help.c",
    "argp-parse.c",
    "argp-pv.c",
    "argp-pvh.c",
]


def build(self):
    from cbuild.util import compiler

    cc = compiler.C(self)
    objs = []
    flags = [
        "-I.",
        "-DHAVE_ALLOCA_H=1",
        "-DHAVE_FLOCKFILE=1",
        "-DHAVE_FUNLOCKFILE=1",
        "-DHAVE_DECL_PROGRAM_INVOCATION_NAME=0",
        "-DHAVE_DECL_PROGRAM_INVOCATION_SHORT_NAME=0",
        "-DHAVE_LIBINTL_H=0",
    ]
    self.mkdir("obj", parents=True)

    for src in _sources:
        obj = "obj/" + src.removesuffix(".c") + ".o"
        cc.invoke([src], obj, obj_file=True, flags=flags)
        objs.append(obj)

    self.do("ar", "rcs", "libargp.a", *objs)


def install(self):
    self.install_file("libargp.a", "usr/lib")
    self.install_file("argp.h", "usr/include")
