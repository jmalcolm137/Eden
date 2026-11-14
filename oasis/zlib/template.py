pkgname = "zlib"
pkgver = "1.3.1"
pkgrel = 0
# Oasis pkg/zlib/src
_commit = "51b7f2abdade71cd9bb0e7a373ef2610ec6f9daf"
pkgdesc = "Compression library"
license = "Zlib"
url = "https://zlib.net"
source = f"https://github.com/madler/zlib/archive/{_commit}.tar.gz"
sha256 = "d9e270d46252734aa49770fbc544125391617956266f220bd63216c834f3a522"
# static-only library, as in the Oasis recipe
options = ["!lto", "!check"]

_sources = [
    "adler32.c", "crc32.c", "deflate.c", "infback.c", "inffast.c",
    "inflate.c", "inftrees.c", "trees.c", "zutil.c", "compress.c",
    "uncompr.c", "gzclose.c", "gzlib.c", "gzread.c", "gzwrite.c",
]


def build(self):
    from cbuild.util import compiler

    cc = compiler.C(self)
    self.mkdir("obj", parents=True)
    objs = []
    flags = [
        "-std=c99", "-Wall", "-Wpedantic",
        "-DHAVE_STDARG_H", "-DHAVE_UNISTD_H", "-D_LARGEFILE64_SOURCE",
    ]
    for src in _sources:
        obj = "obj/" + src.removesuffix(".c") + ".o"
        cc.invoke([src], obj, obj_file=True, flags=flags)
        objs.append(obj)
    self.do("ar", "rcs", "libz.a", *objs)


def install(self):
    self.install_lib("libz.a", mode=0o644)
    self.install_file("zlib.h", "usr/include")
    self.install_file("zconf.h", "usr/include")
    self.install_license("LICENSE")
