pkgname = "farbfeld"
pkgver = "4"
pkgrel = 0
# Oasis pkg/farbfeld/src; GitHub mirror of the same suckless commit
_commit = "ab5e3dfc9cdb476218538c6687df9f44826d8f11"
makedepends = ["libjpeg-turbo", "libpng-devel", "libpng-devel-static", "zlib-static"]
pkgdesc = "Lossless image format and utilities"
license = "ISC"
url = "https://tools.suckless.org/farbfeld"
source = f"https://github.com/mcritchlow/farbfeld/archive/{_commit}.tar.gz"
sha256 = "e1346493c6b15d8e56b8bfcd0a61588c42cbbf4e585f9417ba87cac27f56b23a"
# no test suite in the Oasis recipe
options = ["!check"]

_cflags = ["-std=c99", "-Wall", "-Wextra", "-Wpedantic", "-D_DEFAULT_SOURCE"]
_png_ldflags = ["/usr/lib/libpng.a", "/usr/lib/libz.a"]
_jpg_ldflags = ["/usr/lib/libjpeg-turbo.a"]

_tools = {
    "png2ff": _png_ldflags,
    "ff2png": _png_ldflags,
    "jpg2ff": _jpg_ldflags,
    "ff2jpg": _jpg_ldflags,
    "ff2pam": [],
    "ff2ppm": [],
}


def build(self):
    from cbuild.util import compiler

    cc = compiler.C(self)
    self.mkdir("obj", parents=True)
    cc.invoke(["util.c"], "obj/util.o", obj_file=True, flags=_cflags)
    for name, ldflags in _tools.items():
        cc.invoke(
            [f"{name}.c", "obj/util.o"],
            name,
            flags=_cflags,
            ldflags=ldflags,
        )


def install(self):
    for name in _tools:
        self.install_bin(name)
        self.install_man(f"{name}.1")
    self.install_man("farbfeld.5")
    self.install_license("LICENSE")
