pkgname = "wld"
pkgver = "0_git20200101"
pkgrel = 0
# Oasis pkg/wld/src
_commit = "3fe15e769cf81784215c003b18438184083af8ce"
makedepends = [
    "fontconfig-devel",
    "freetype",
    "libdrm-devel",
    "linux-headers",
    "pixman",
    "wayland",
    "wayland-protocols",
]
pkgdesc = "Wayland display library"
license = "MIT"
url = "https://github.com/michaelforney/wld"
source = f"{url}/archive/{_commit}.tar.gz"
sha256 = "e0c1ec03dd8e840ae3fb28b3e904dba2dd76e76808fe094e9ad1bf041f110f4e"
# static-only library, as in the Oasis recipe
options = ["!lto", "!check"]

_cflags = [
    "-DWITH_WAYLAND_SHM",
    "-DWITH_WAYLAND_DRM",
    "-iquote",".",
    "-I/usr/include/freetype2",
    "-I/usr/include",
    "-I/usr/include/libdrm",
    "-I/usr/include/pixman-1",
]

_sources = [
    "buffer.c",
    "buffered_surface.c",
    "color.c",
    "context.c",
    "drm.c",
    "dumb.c",
    "font.c",
    "renderer.c",
    "surface.c",
    "pixman.c",
    "wayland.c",
    "wayland-shm.c",
    "wayland-drm.c",
]


def pre_build(self):
    self.do(
        "wayland-scanner",
        "client-header",
        "protocol/wayland-drm.xml",
        "protocol/wayland-drm-client-protocol.h",
    )
    self.do(
        "wayland-scanner",
        "private-code",
        "protocol/wayland-drm.xml",
        "protocol/wayland-drm-protocol.c",
    )


def build(self):
    from cbuild.util import compiler

    cc = compiler.C(self)
    self.mkdir("obj", parents=True)
    objs = []
    for src in _sources:
        obj = "obj/" + src.replace("/", "_").removesuffix(".c") + ".o"
        cc.invoke([src], obj, obj_file=True, flags=_cflags)
        objs.append(obj)
    obj = "obj/wayland-drm-protocol.o"
    cc.invoke(["protocol/wayland-drm-protocol.c"], obj, obj_file=True, flags=_cflags)
    objs.append(obj)
    self.do("ar", "rcs", "libwld.a", *objs)


def install(self):
    self.install_lib("libwld.a", mode=0o644)
    for h in ("wld.h", "drm.h", "pixman.h", "wayland.h"):
        self.install_file(h, "usr/include/wld")
    self.install_license("COPYING")


@subpackage("wld-devel")
def _(self):
    return ["usr/include"]
