pkgname = "fspec-sync"
pkgver = "0_git20221127"
pkgrel = 0
_commit = "a79592936c865e001ac3003dddc5f60f0bada97e"
makedepends = ["b3sum-devel", "b3sum-devel-static"]
pkgdesc = "Filesystem spec sync tools"
license = "custom:fspec-sync"
url = "https://github.com/oasislinux/fspec-sync"
source = f"https://github.com/oasislinux/fspec-sync/archive/{_commit}.tar.gz"
sha256 = "3c2a117b69589110967b0e4f87586fb79a0c494735d6eced26c4bc186e2e2489"
# no test suite in the Oasis recipe
options = ["!check"]

_cflags = ["-std=c99", "-Wall", "-Wpedantic", "-Wno-maybe-uninitialized"]


def build(self):
    from cbuild.util import compiler

    cc = compiler.C(self)
    common = []
    for src in ["fatal.c", "parse.c", "reallocarray.c"]:
        obj = src + ".o"
        cc.invoke([src], obj, obj_file=True, flags=_cflags)
        common.append(obj)
    self.do("ar", "rcs", "libcommon.a", *common)
    for exe, srcs in [
        ("fspec-hash", ["fspec-hash.c", "libcommon.a", "/usr/lib/libblake3.a"]),
        ("fspec-sort", ["fspec-sort.c", "libcommon.a"]),
        ("fspec-tar", ["fspec-tar.c", "libcommon.a"]),
    ]:
        cc.invoke(srcs, exe, flags=_cflags)


def install(self):
    self.install_bin("fspec-hash")
    self.install_bin("fspec-sort")
    self.install_bin("fspec-tar")
    self.install_license("LICENSE")
