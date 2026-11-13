pkgname = "libnl"
pkgver = "3.5.0"
pkgrel = 2
# Oasis pkg/libnl/src
_commit = "7b167ef85f6eb4d7faca349302478b2dc121e309"
makedepends = ["linux-headers"]
pkgdesc = "Netlink protocol library"
license = "LGPL-2.1-or-later"
url = "https://www.infradead.org/~tgr/libnl"
source = f"https://github.com/thom311/libnl/archive/{_commit}.tar.gz"
sha256 = "b5fcf87ee280971112c581704a4b9ff25cb982b84da5ab5d9503d0eccff879fe"
# static-only library, as in the Oasis recipe
options = ["!lto", "!check"]

_cflags = [
    "-D_GNU_SOURCE",
    '-DSYSCONFDIR="/etc/libnl"',
    "-I.",
    "-Iinclude",
    "-Iinclude/linux-private",
]

_lib_sources = [
    "addr.c",
    "attr.c",
    "cache.c",
    "cache_mngr.c",
    "cache_mngt.c",
    "data.c",
    "error.c",
    "handlers.c",
    "msg.c",
    "nl.c",
    "object.c",
    "socket.c",
    "utils.c",
    "version.c",
    "hash.c",
    "hashtable.c",
    "mpls.c",
]


def pre_build(self):
    self.cp(self.files_path / "defs.h", "defs.h")
    self.mkdir("include/netlink", parents=True)
    src = self.cwd / "include/netlink/version.h.in"
    text = src.read_text()
    for key, val in {
        "@PACKAGE_STRING@": '"libnl 3.5.0"',
        "@PACKAGE_VERSION@": "3.5.0",
        "@MAJ_VERSION@": "3",
        "@MIN_VERSION@": "5",
        "@MIC_VERSION@": "0",
        "@LT_CURRENT@": "226",
        "@LT_REVISION@": "0",
        "@LT_AGE@": "26",
    }.items():
        text = text.replace(key, val)
    (self.cwd / "include/netlink/version.h").write_text(text)


def build(self):
    from cbuild.util import compiler

    cc = compiler.C(self)
    self.mkdir("obj", parents=True)
    objs = []
    for src in _lib_sources:
        obj = "obj/" + src.removesuffix(".c") + ".o"
        cc.invoke([f"lib/{src}"], obj, obj_file=True, flags=_cflags)
        objs.append(obj)
    self.do("ar", "rcs", "libnl-3.a", *objs)

    gobjs = []
    for src in ["ctrl.c", "family.c", "genl.c", "mngt.c"]:
        obj = "obj/genl-" + src.removesuffix(".c") + ".o"
        cc.invoke([f"lib/genl/{src}"], obj, obj_file=True, flags=_cflags)
        gobjs.append(obj)
    self.do("ar", "rcs", "libnl-genl-3.a", *gobjs)


def install(self):
    self.install_lib("libnl-3.a", mode=0o644)
    self.install_lib("libnl-genl-3.a", mode=0o644)
    for h in [
        "addr.h",
        "attr.h",
        "cache.h",
        "cache-api.h",
        "data.h",
        "errno.h",
        "handlers.h",
        "hash.h",
        "hashtable.h",
        "list.h",
        "msg.h",
        "netlink.h",
        "netlink-compat.h",
        "netlink-kernel.h",
        "object.h",
        "object-api.h",
        "socket.h",
        "types.h",
        "utils.h",
        "version.h",
        "genl/ctrl.h",
        "genl/family.h",
        "genl/genl.h",
        "genl/mngt.h",
    ]:
        self.install_file(f"include/netlink/{h}", "usr/include/netlink")
    self.install_license("COPYING")


@subpackage("libnl-devel")
def _(self):
    return ["usr/include"]
