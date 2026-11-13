pkgname = "libgpiod"
pkgver = "1.6.3"
pkgrel = 1
# Oasis pkg/libgpiod/src
_commit = "bb4e5ce7071feed41bd3f0d9a62b5033fd483a18"
makedepends = ["linux-headers"]
pkgdesc = "Library and tools for GPIO character devices"
license = "LGPL-2.1-or-later"
url = "https://git.kernel.org/pub/scm/libs/libgpiod/libgpiod.git"
source = f"{url}/snapshot/libgpiod-{_commit}.tar.gz"
sha256 = "218aefafc0fd8fb14d6a4acc6506f55ebe69d9182cab86a272c1a6a733af8f9c"
# static-only library, as in the Oasis recipe
options = ["!lto", "!check"]

_cflags = [
    "-std=c99",
    "-D_GNU_SOURCE",
    "-Wall",
    "-Wextra",
    "-Wpedantic",
    "-Wno-overflow",
    "-Iinclude",
    "-include",
    "config.h",
    "-include",
    "libgen.h",
]

_tools = ["gpiodetect", "gpioinfo", "gpioget", "gpioset", "gpiomon", "gpiofind"]


def pre_build(self):
    self.cp(self.files_path / "config.h", "config.h")


def build(self):
    from cbuild.util import compiler

    cc = compiler.C(self)
    self.mkdir("obj", parents=True)
    objs = []
    for src in ["core.c", "ctxless.c", "helpers.c", "iter.c", "misc.c"]:
        obj = "obj/" + src.removesuffix(".c") + ".o"
        cc.invoke([f"lib/{src}"], obj, obj_file=True, flags=_cflags)
        objs.append(obj)
    self.do("ar", "rcs", "libgpiod.a", *objs)

    cc.invoke(
        ["tools/tools-common.c"], "obj/tools-common.o", obj_file=True, flags=_cflags
    )
    for tool in _tools:
        cc.invoke(
            [f"tools/{tool}.c", "obj/tools-common.o", "libgpiod.a"],
            tool,
            flags=_cflags,
        )


def install(self):
    self.install_lib("libgpiod.a", mode=0o644)
    for h in ["gpiod.h"]:
        self.install_file(f"include/{h}", "usr/include")
    for tool in _tools:
        self.install_bin(tool)
    self.install_license("COPYING")


@subpackage("libgpiod-devel")
def _(self):
    return ["usr/include"]
