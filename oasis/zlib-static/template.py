pkgname = "zlib-static"
pkgver = "1.3.1"
pkgrel = 0
# Oasis pkg/zlib/src
_commit = "51b7f2abdade71cd9bb0e7a373ef2610ec6f9daf"
pkgdesc = "Compression library from Oasis"
license = "Zlib"
url = "https://zlib.net"
source = f"https://github.com/madler/zlib/archive/{_commit}.tar.gz"
sha256 = "d9e270d46252734aa49770fbc544125391617956266f220bd63216c834f3a522"
# no test suite
options = ["!check", "!lto"]

_sources = [
    "adler32.c",
    "crc32.c",
    "deflate.c",
    "infback.c",
    "inffast.c",
    "inflate.c",
    "inftrees.c",
    "trees.c",
    "zutil.c",
    "compress.c",
    "uncompr.c",
    "gzclose.c",
    "gzlib.c",
    "gzread.c",
    "gzwrite.c",
]


def build(self):
    from cbuild.util import compiler

    cc = compiler.C(self)
    objs = []
    flags = [
        "-std=c99",
        "-Wall",
        "-Wpedantic",
        "-DHAVE_STDARG_H",
        "-DHAVE_UNISTD_H",
        "-D_LARGEFILE64_SOURCE",
    ]
    self.mkdir("obj", parents=True)

    for src in _sources:
        obj = "obj/" + src.removesuffix(".c") + ".o"
        cc.invoke([src], obj, obj_file=True, flags=flags)
        objs.append(obj)

    self.do("ar", "rcs", "libz.a", *objs)


def install(self):
    self.install_file("libz.a", "usr/lib")
    self.install_file("zlib.h", "usr/include")
    self.install_file("zconf.h", "usr/include")
    self.install_license("LICENSE")
