pkgname = "b3sum"
pkgver = "1.5.0"
pkgrel = 0
_commit = "d995c3d31b42d09a568a0a658bcbcd3814164ca9"
pkgdesc = "BLAKE3 checksum tool"
license = "CC0-1.0"
url = "https://git.sr.ht/~mcf/b3sum"
source = f"https://git.sr.ht/~mcf/b3sum/archive/{_commit}.tar.gz"
sha256 = "705b465fec6f59240f521faf94379f9ae465f2907a15f80b9b2b815a91f69e02"
# no test suite in the Oasis recipe
options = ["!check"]

_cflags = ["-std=c99", "-Wall", "-Wpedantic", "-DWITH_ASM"]

_libsrc = [
    "blake3.c",
    "blake3_dispatch.c",
    "blake3_portable.c",
    "blake3_cpuid.S",
    "blake3_avx2_x86-64_unix.S",
    "blake3_avx512_x86-64_unix.S",
    "blake3_sse2_x86-64_unix.S",
    "blake3_sse41_x86-64_unix.S",
]


def build(self):
    from cbuild.util import compiler

    cc = compiler.C(self)
    objs = []
    for src in _libsrc:
        obj = src + ".o"
        cc.invoke([src], obj, obj_file=True, flags=_cflags)
        objs.append(obj)
    self.do("ar", "rcs", "libblake3.a", *objs)
    cc.invoke(["b3sum.c", "libblake3.a"], "b3sum", flags=_cflags)


def install(self):
    self.install_bin("b3sum")
    self.install_man("b3sum.1")
    self.install_license("LICENSE")
    self.install_file("blake3.h", "usr/include")
    self.install_lib("libblake3.a")


@subpackage("b3sum-devel")
def _(self):
    self.depends = [self.parent]
    return ["usr/include/blake3.h", "usr/lib/libblake3.a"]
