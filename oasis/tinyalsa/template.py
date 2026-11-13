pkgname = "tinyalsa"
pkgver = "2.0.0"
pkgrel = 1
# Oasis pkg/tinyalsa/src; Oasis ver 2.0.0-45-g4fbaeef
_commit = "4fbaeef03cd1cb216e0f356c0433ca70f8b9c464"
makedepends = ["linux-headers"]
pkgdesc = "Tiny ALSA library and utilities"
license = "BSD-3-Clause"
url = "https://github.com/tinyalsa/tinyalsa"
source = f"{url}/archive/{_commit}.tar.gz"
sha256 = "b9659b6e77dba4b11a6cc56fe9a1f6392d20db45f6d558fa8649c40da3de5d41"
# no test suite in the Oasis recipe
options = ["!check"]

_cflags = [
    "-std=c99",
    "-Wall",
    "-Wpedantic",
    "-Wno-overflow",
    "-D_POSIX_C_SOURCE=201112L",
    "-Iinclude",
]

_lib_sources = [
    "limits.c",
    "pcm.c",
    "pcm_hw.c",
    "mixer.c",
    "mixer_hw.c",
    "snd_card_plugin.c",
]

_tools = ["tinycap", "tinymix", "tinypcminfo", "tinyplay"]


def build(self):
    from cbuild.util import compiler

    cc = compiler.C(self)
    self.mkdir("obj", parents=True)
    objs = []
    for src in _lib_sources:
        obj = "obj/" + src.removesuffix(".c") + ".o"
        cc.invoke([f"src/{src}"], obj, obj_file=True, flags=_cflags)
        objs.append(obj)
    self.do("ar", "rcs", "libtinyalsa.a", *objs)

    for tool in _tools:
        cc.invoke([f"utils/{tool}.c", "libtinyalsa.a"], tool, flags=_cflags)


def install(self):
    self.install_lib("libtinyalsa.a", mode=0o644)
    for h in [
        "attributes.h",
        "pcm.h",
        "mixer.h",
        "asoundlib.h",
        "version.h",
    ]:
        self.install_file(f"include/tinyalsa/{h}", "usr/include/tinyalsa")
    for tool in _tools:
        self.install_bin(tool)
        self.install_man(f"utils/{tool}.1")
    self.install_license("LICENSE")


@subpackage("tinyalsa-devel")
def _(self):
    return ["usr/include"]


@subpackage("tinyalsa-devel-static")
def _(self):
    return ["usr/lib/*.a"]
