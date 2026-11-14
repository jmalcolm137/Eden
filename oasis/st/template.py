pkgname = "st"
pkgver = "0_git20200101"
pkgrel = 7
makedepends = [
    "e2fsprogs-devel-static",
    "expat",
    "fontconfig-devel",
    "freetype",
    "libdrm-devel-static",
    "libffi8-devel-static",
    "libxkbcommon",
    "linux-headers",
    "pixman",
    "wayland",
    "wayland-protocols",
    "wld",
    "wld-devel",
    "zlib-static",
]
pkgdesc = "Simple terminal emulator"
license = "MIT"
url = "https://st.suckless.org"
# source is the Oasis-pinned suckless commit, vendored under files/
# no test suite in the Oasis recipe
options = ["!check"]

_cflags = [
    "-DVERSION=\"0.7\"",
    "-I.",
    "-I/usr/include/freetype2",
    "-I/usr/include/pixman-1",
    "-I/usr/include/xkbcommon",
]

_files = ["st.c", "arg.h", "config.h", "config.def.h", "config.mk", "Makefile", "st.1", "LICENSE"]


def pre_build(self):
    for name in _files:
        self.cp(self.files_path / name, name)
    for patch in sorted((self.files_path / "patches").glob("*.patch")):
        self.cp(patch, patch.name)
        self.do("patch", "-p1", "-i", patch.name)
    self.do(
        "wayland-scanner",
        "client-header",
        "/usr/share/wayland-protocols/stable/xdg-shell/xdg-shell.xml",
        "xdg-shell-client-protocol.h",
    )
    self.do(
        "wayland-scanner",
        "private-code",
        "/usr/share/wayland-protocols/stable/xdg-shell/xdg-shell.xml",
        "xdg-shell-protocol.c",
    )


def build(self):
    from cbuild.util import compiler

    cc = compiler.C(self)
    cc.invoke(
        ["st.c", "xdg-shell-protocol.c"],
        "st",
        flags=_cflags,
        ldflags=[
            "/usr/lib/libxkbcommon.a",
            "/usr/lib/libwayland-client.a",
            "/usr/lib/libwayland-cursor.a",
            "/usr/lib/libwld.a",
            "/usr/lib/libfontconfig.a",
            "/usr/lib/libfreetype.a",
            "/usr/lib/libpixman.a",
            "/usr/lib/libz.a",
            "/usr/lib/libexpat.a",
            "/usr/lib/libuuid.a",
            "/usr/lib/libdrm.a",
            "/usr/lib/libffi.a",
            "-lm",
            "-lpthread",
            "-ldl",
        ],
    )


def install(self):
    self.install_bin("st")
    self.install_man("st.1")
    self.install_license("LICENSE")
