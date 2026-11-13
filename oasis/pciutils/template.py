pkgname = "pciutils"
pkgver = "3.14.0"
pkgrel = 0
# Oasis pkg/pciutils/src
_commit = "c6030ae1576b6bf1de9b41f53a9ed76137181d99"
makedepends = ["linux-headers"]
pkgdesc = "PCI utilities"
license = "GPL-2.0-or-later"
url = "https://mj.ucw.cz/sw/pciutils"
source = f"https://git.kernel.org/pub/scm/utils/pciutils/pciutils.git/snapshot/pciutils-{_commit}.tar.gz"
sha256 = "253f34a5ecc6a5ea199fda11e1a193433438531d9e2fd9ca3855beafa340b4fc"
# static-only library, as in the Oasis recipe
options = ["!lto", "!check"]

_cflags = ["-Wall", "-Wpedantic", "-Wno-parentheses", "-I.", "-Ilib"]

_lib_sources = [
    "init.c",
    "access.c",
    "generic.c",
    "dump.c",
    "names.c",
    "filter.c",
    "names-hash.c",
    "names-parse.c",
    "names-net.c",
    "names-cache.c",
    "names-hwdb.c",
    "params.c",
    "caps.c",
    "sysfs.c",
]


def pre_build(self):
    self.cp(self.files_path / "config.h", "config.h")


def build(self):
    from cbuild.util import compiler

    cc = compiler.C(self)
    self.mkdir("obj", parents=True)
    objs = []
    for src in _lib_sources:
        obj = "obj/" + src.removesuffix(".c") + ".o"
        cc.invoke([f"lib/{src}"], obj, obj_file=True, flags=_cflags)
        objs.append(obj)
    self.do("ar", "rcs", "libpci.a", *objs)

    cc.invoke(["common.c"], "obj/common.o", obj_file=True, flags=_cflags)
    cc.invoke(
        [
            "lspci.c",
            "ls-vpd.c",
            "ls-caps.c",
            "ls-caps-vendor.c",
            "ls-ecaps.c",
            "ls-kernel.c",
            "ls-tree.c",
            "ls-map.c",
            "obj/common.o",
            "libpci.a",
        ],
        "lspci",
        flags=_cflags,
    )
    cc.invoke(["setpci.c", "obj/common.o", "libpci.a"], "setpci", flags=_cflags)


def install(self):
    self.install_bin("lspci")
    self.install_bin("setpci")
    self.install_man("lspci.man", cat=8)
    self.install_man("setpci.man", cat=8)
    self.install_man("pci.ids.man", cat=5)
    self.install_file("pci.ids", "usr/share")
    self.install_lib("libpci.a", mode=0o644)
    self.install_file("lib/pci.h", "usr/include")
    self.install_license("COPYING")


@subpackage("pciutils-devel")
def _(self):
    return ["usr/include"]
