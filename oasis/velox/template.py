pkgname = "velox"
pkgver = "0_git20201110"
pkgrel = 3
# Oasis pkg/velox/src
_commit = "2ae5e99dfcccfc10f98b3e1a697201db4a8676f8"
hostmakedepends = ["wayland-progs"]
makedepends = [
    "fontconfig-devel",
    "libatomic-chimera-devel-static",
    "libdrm-devel",
    "libdrm-devel-static",
    "libevdev-devel",
    "libevdev-devel-static",
    "libinput-devel",
    "libinput-devel-static",
    "libunwind-devel-static",
    "libxkbcommon-devel",
    "libxkbcommon-devel-static",
    "linux-headers",
    "mtdev",
    "mtdev-devel",
    "musl-devel-static",
    "pixman-devel",
    "swc",
    "swc-devel",
    "udev-devel",
    "udev-devel-static",
    "wayland-devel",
    "wayland-devel-static",
    "wld",
    "wld-devel",
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

    self.do(
        "wayland-scanner", "client-header", "protocol/velox.xml",
        "protocol/velox-client-protocol.h",
    )
    self.do(
        "wayland-scanner", "server-header", "protocol/velox.xml",
        "protocol/velox-server-protocol.h",
    )
    self.do(
        "wayland-scanner", "private-code", "protocol/velox.xml",
        "protocol/velox-protocol.c",
    )

    cc = compiler.C(self)
    flags = [
        "-std=c99",
        "-D_GNU_SOURCE",
        '-DVELOX_LIBEXEC="/usr/lib/velox"',
        "-I.",
        "-I/usr/include/pixman-1",
        "-I/usr/include/freetype2",
    ]
    self.mkdir("obj", parents=True)

    objs = []
    for src in [*_sources, "protocol/velox-protocol.c"]:
        obj = "obj/" + src.rsplit("/", 1)[-1].removesuffix(".c") + ".o"
        cc.invoke([src], obj, obj_file=True, flags=flags)
        objs.append(obj)

    cc.invoke(
        objs,
        "velox",
        flags=flags,
        ldflags=[
            "-static-pie",
            "-lswc",
            "/usr/lib/libwayland-server.a",
            "/usr/lib/libpixman-1.a",
            "/usr/lib/libpng16.a",
            "-lm",
            "-ldl",
            "-lpthread",
            "-lrt",
        ],
    )

    # the Lua recipe also builds the static status_bar helper
    self.do("cp", "/usr/share/swc/swc-protocol.c", "swc-protocol.c")
    self.do(
        "cp",
        "/usr/include/swc-client-protocol.h",
        "protocol/swc-client-protocol.h",
    )
    cc.invoke(
        ["clients/status_bar.c", "protocol/velox-protocol.c", "swc-protocol.c"],
        "status_bar",
        flags=flags,
        ldflags=[
            "-static-pie",
            "-lswc",
            "/usr/lib/libwayland-client.a",
            "/usr/lib/libpixman-1.a",
            "/usr/lib/libpng16.a",
            "-lm",
            "-ldl",
            "-lpthread",
            "-lrt",
        ],
    )


def install(self):
    self.install_bin("velox")
    self.install_file("status_bar", "usr/lib/velox", mode=0o755)
    self.install_file("velox.conf.sample", "usr/share/doc/velox")
    self.install_license("LICENSE")
