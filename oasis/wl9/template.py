pkgname = "wl9"
pkgver = "0_git20221119"
pkgrel = 1
# Oasis pkg/wl9/src
_commit = "de70033524ef21dd01bde1d5d66a4679c8f34311"
makedepends = [
    "libatomic-chimera-devel-static",
    "libffi8-devel-static",
    "libunwind-devel-static",
    "musl-devel-static",
    "wayland-devel",
    "wayland-devel-static",
    "wayland-protocols",
]
pkgdesc = "Plan 9-style window manager for Wayland"
license = "ISC"
url = "https://git.sr.ht/~mcf/wl9"
source = f"{url}/archive/{_commit}.tar.gz"
sha256 = "3a8cb561ae97c095763d67ff18b0b48cbcd5502805b59736948c905d5f602d21"
# no test suite in the Oasis recipe
options = ["!check"]

_cflags = [
    "-std=c11",
    "-Wall",
    "-Wpedantic",
    "-Wno-parentheses",
    "-I.",
]


def build(self):
    from cbuild.util import compiler

    cc = compiler.C(self)
    cc.invoke(
        [
            "wl9.c",
            "c9.c",
            "fs.c",
            "util.c",
            "keymap.c",
            "server-decoration-protocol.c",
            "xdg-shell-protocol.c",
        ],
        "wl9",
        flags=_cflags,
        ldflags=[
            "-static-pie",
            "/usr/lib/libwayland-server.a",
            "/usr/lib/libffi.a",
        ],
    )


def install(self):
    self.install_bin("wl9")
    self.install_license("LICENSE")
