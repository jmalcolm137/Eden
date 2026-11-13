pkgname = "mtdev"
pkgver = "1.1.7"
pkgrel = 0
makedepends = ["linux-headers"]
pkgdesc = "Multitouch protocol translation library"
license = "MIT"
url = "https://bitmath.se/org/code/mtdev"
source = f"{url}/mtdev-{pkgver}.tar.gz"
sha256 = "a55bd02a9af4dd266c0042ec608744fff3a017577614c057da09f1f4566ea32c"
# static-only library, as in the Oasis recipe
options = ["!lto", "!check"]

_cflags = ["-Iinclude"]


def build(self):
    from cbuild.util import compiler

    cc = compiler.C(self)
    self.mkdir("obj", parents=True)
    objs = []
    for src in ["caps.c", "core.c", "iobuf.c", "match.c", "match_four.c"]:
        obj = "obj/" + src.removesuffix(".c") + ".o"
        cc.invoke([f"src/{src}"], obj, obj_file=True, flags=_cflags)
        objs.append(obj)
    self.do("ar", "rcs", "libmtdev.a", *objs)


def install(self):
    self.install_lib("libmtdev.a", mode=0o644)
    self.install_file("include/mtdev.h", "usr/include")
    self.install_file("include/mtdev-plumbing.h", "usr/include")
    self.install_license("COPYING")


@subpackage("mtdev-devel")
def _(self):
    return ["usr/include"]
