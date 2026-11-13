pkgname = "libutp"
pkgver = "0_git20200101"
pkgrel = 0
# Oasis pkg/libutp/src
_commit = "996ad97f18a09a2f3d38cb210a44014eaf089df5"
pkgdesc = "Micro Transport Protocol library"
license = "MIT"
url = "https://github.com/oasislinux/libutp"
source = f"{url}/archive/{_commit}.tar.gz"
sha256 = "a1e1fd88754407290ba29ab79a2169ab4c8d66c57245b90b4b901899d2318004"
# static-only library, as in the Oasis recipe
options = ["!lto", "!check"]

_cflags = ["-std=c99", "-Wall", "-Wpedantic", "-D_POSIX_C_SOURCE=200809L", "-I."]


def build(self):
    from cbuild.util import compiler

    cc = compiler.C(self)
    self.mkdir("obj", parents=True)
    objs = []
    for src in ("utp.c", "utp_utils.c"):
        obj = "obj/" + src.removesuffix(".c") + ".o"
        cc.invoke([src], obj, obj_file=True, flags=_cflags)
        objs.append(obj)
    self.do("ar", "rcs", "libutp.a", *objs)


def install(self):
    self.install_lib("libutp.a", mode=0o644)
    self.install_file("utp.h", "usr/include/libutp")
    self.install_license("LICENSE")


@subpackage("libutp-devel")
def _(self):
    return ["usr/include"]
