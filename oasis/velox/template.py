pkgname = "velox"
pkgver = "0_git20201110"
pkgrel = 0
# Oasis pkg/velox/src
_commit = "2ae5e99dfcccfc10f98b3e1a697201db4a8676f8"
hostmakedepends = ["wayland"]
makedepends = [
    "fontconfig",
    "libdrm",
    "libevdev",
    "libinput",
    "libxkbcommon",
    "linux-headers",
    "mtdev",
    "pixman",
    "swc",
    "util-linux",
    "wayland",
    "wld",
]
pkgdesc = "Wayland compositor from Oasis"
license = "MIT"
url = "https://github.com/michaelforney/velox"
source = f"{url}/archive/{_commit}.tar.gz"
sha256 = "7390124152b1a59e88ae5781393ae651bbd51a2458ee4dc867a095c5640d5356"
# no test suite
options = ["!check"]

_sources = [
    "config.c",
    "layout.c",
    "screen.c",
    "tag.c",
    "util.c",
    "velox.c",
    "window.c",
]


def build(self):
    from cbuild.util import compiler

    self.mkdir("gen", parents=True)
    self.do(
        "wayland-scanner", "client-header", "protocol/velox.xml",
        "gen/velox-client-protocol.h",
    )
    self.do(
        "wayland-scanner", "server-header", "protocol/velox.xml",
        "gen/velox-server-protocol.h",
    )
    self.do(
        "wayland-scanner", "private-code", "protocol/velox.xml",
        "gen/velox-protocol.c",
    )

    cc = compiler.C(self)
    flags = [
        "-std=c99",
        "-D_GNU_SOURCE",
        '-DVELOX_LIBEXEC="/usr/lib/velox"',
        "-I.",
        "-Igen",
        "-I/usr/include/pixman-1",
        "-I/usr/include/freetype2",
    ]
    self.mkdir("obj", parents=True)

    objs = []
    for src in _sources + ["gen/velox-protocol.c"]:
        obj = "obj/" + src.rsplit("/", 1)[-1].removesuffix(".c") + ".o"
        cc.invoke([src], obj, obj_file=True, flags=flags)
        objs.append(obj)

    cc.invoke(
        objs,
        "velox",
        flags=flags,
        ldflags=[
            "-Wl,--start-group",
            "-lswc",
            "-lwld",
            "-lwayland-server",
            "-lwayland-client",
            "-linput",
            "-lxkbcommon",
            "-lpixman",
            "-lfontconfig",
            "-lfreetype",
            "-lexpat",
            "-ldrm",
            "-levdev",
            "-lmtdev",
            "-luuid",
            "-Wl,--end-group",
            "-lm",
            "-ldl",
        ],
    )


def install(self):
    self.install_bin("velox")
    self.install_file("velox.conf.sample", "usr/share/doc/velox")
    self.install_license("LICENSE")
