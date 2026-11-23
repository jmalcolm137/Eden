pkgname = "dmenu"
pkgver = "4.9"
pkgrel = 5
makedepends = [
    "e2fsprogs-devel-static",
    "fontconfig-devel",
    "fontconfig-devel-static",
    "freetype-devel",
    "freetype-devel-static",
    "libatomic-chimera-devel-static",
    "libdrm-devel-static",
    "libexpat-devel",
    "libexpat-devel-static",
    "libffi8-devel-static",
    "libunwind-devel-static",
    "libxkbcommon-devel",
    "libxkbcommon-devel-static",
    "musl-devel-static",
    "pixman-devel",
    "pixman-devel-static",
    "swc",
    "swc-devel",
    "udev-devel",
    "wayland-devel",
    "wayland-devel-static",
    "wayland-progs",
    "wayland-protocols",
    "wld",
    "wld-devel",
    "zlib",
]
pkgdesc = "Dynamic menu"
license = "MIT"
url = "https://tools.suckless.org/dmenu"
# source is the Oasis-pinned suckless commit, vendored under files/
options = ["!check"]

_cflags = [
    "-std=c99", "-Wall", "-Wpedantic", "-Wno-maybe-uninitialized",
    "-D_POSIX_C_SOURCE=200809L", '-DVERSION="4.6"', "-I.",
    "-I/usr/include/freetype2", "-I/usr/include/pixman-1",
    "-I/usr/include/xkbcommon",
]

_files = [
    "dmenu.c", "drw.c", "drw.h", "util.c", "util.h", "stest.c", "arg.h",
    "config.h", "config.def.h", "config.mk", "Makefile", "dmenu.1", "stest.1",
    "dmenu_path", "dmenu_run", "LICENSE",
]

_ldflags = [
    "-static-pie",
    "/usr/lib/libswc.a",
    "/usr/lib/libwayland-client.a",
    "-lm",
    "-lpthread",
    "-ldl",
    "-lrt",
]


def pre_build(self):
    for name in _files:
        self.cp(self.files_path / name, name)
    for patch in sorted((self.files_path / "patches").glob("*.patch")):
        self.cp(patch, patch.name)
        self.do("patch", "-p1", "-i", patch.name)
    self.do(
        "wayland-scanner", "client-header",
        "/usr/share/swc/swc.xml", "swc-client-protocol.h",
    )
    self.do(
        "wayland-scanner", "private-code",
        "/usr/share/swc/swc.xml", "swc-protocol.c",
    )


def build(self):
    from cbuild.util import compiler

    cc = compiler.C(self)
    cc.invoke(
        ["dmenu.c", "drw.c", "util.c", "swc-protocol.c"],
        "dmenu",
        flags=_cflags,
        ldflags=_ldflags,
    )
    cc.invoke(
        ["stest.c"], "stest", flags=_cflags, ldflags=["-static-pie"]
    )


def install(self):
    self.install_bin("dmenu")
    self.install_bin("stest")
    self.install_bin("dmenu_path")
    self.install_bin("dmenu_run")
    self.install_man("dmenu.1")
    self.install_man("stest.1")
    self.install_license("LICENSE")
