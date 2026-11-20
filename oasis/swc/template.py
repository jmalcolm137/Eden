pkgname = "swc"
pkgver = "0_git20200101"
pkgrel = 3
# Oasis pkg/swc/src
_commit = "19893a5ca3239082b904a04fdb9ac7c3a1fb62e2"
makedepends = [
    "fontconfig-devel",
    "fontconfig-devel-static",
    "freetype-devel",
    "freetype-devel-static",
    "gettext-devel-static",
    "libatomic-chimera-devel-static",
    "libdrm-devel",
    "libdrm-devel-static",
    "libevdev-devel",
    "libevdev-devel-static",
    "libexpat-devel-static",
    "libffi8-devel-static",
    "libinput-devel",
    "libinput-devel-static",
    "libunwind-devel-static",
    "libxkbcommon-devel",
    "libxkbcommon-devel-static",
    "libxml2-devel-static",
    "linux-headers",
    "mtdev",
    "mtdev-devel",
    "musl-devel-static",
    "pixman-devel",
    "pixman-devel-static",
    "udev-devel",
    "udev-devel-static",
    "wayland-devel",
    "wayland-devel-static",
    "wayland-progs",
    "wayland-protocols",
    "wld",
    "wld-devel",
    "zlib-static",
]
pkgdesc = "Wayland compositor library"
license = "MIT"
url = "https://github.com/michaelforney/swc"
source = f"{url}/archive/{_commit}.tar.gz"
sha256 = "d359df126b40296f6f90d680987f7757c6f50ddd1e7b94f7f5fb21a85a73815d"
# no test suite in the Oasis recipe
options = ["!lto", "!check", "!strip"]

_cflags = [
    "-Wall", "-D_GNU_SOURCE", "-DENABLE_LIBUDEV",
    "-Dscreen_new=swc__screen_new",
    "-Dremove_resource=swc__remove_resource",
    "-I.", "-Iinclude",
    "-I/usr/include/libdrm",
    "-I/usr/include/freetype2",
    "-I/usr/include/pixman-1",
    "-I/usr/include/xkbcommon",
]

_lib_sources = [
    "libswc/bindings.c", "libswc/compositor.c", "libswc/data.c",
    "libswc/data_device.c", "libswc/data_device_manager.c", "libswc/dmabuf.c",
    "libswc/drm.c", "libswc/input.c", "libswc/kde_decoration.c",
    "libswc/keyboard.c", "libswc/launch.c", "libswc/mode.c", "libswc/output.c",
    "libswc/panel.c", "libswc/panel_manager.c", "libswc/plane.c",
    "libswc/pointer.c", "libswc/primary_plane.c", "libswc/region.c",
    "libswc/screen.c", "libswc/shell.c", "libswc/shell_surface.c",
    "libswc/seat.c", "libswc/shm.c", "libswc/subcompositor.c",
    "libswc/subsurface.c", "libswc/surface.c", "libswc/swc.c",
    "libswc/util.c", "libswc/view.c", "libswc/wayland_buffer.c",
    "libswc/window.c", "libswc/xdg_decoration.c", "libswc/xdg_shell.c",
]


def pre_build(self):
    self.mkdir("include", parents=True)
    self.mkdir("cursor", parents=True)
    cmds = [
        ("client-header", "protocol/swc.xml", "include/swc-client-protocol.h"),
        ("server-header", "protocol/swc.xml", "include/swc-server-protocol.h"),
        ("private-code", "protocol/swc.xml", "swc-protocol.c"),
        ("server-header", "protocol/server-decoration.xml", "include/server-decoration-server-protocol.h"),
        ("private-code", "protocol/server-decoration.xml", "server-decoration-protocol.c"),
        ("server-header", "/usr/share/wayland-protocols/stable/xdg-shell/xdg-shell.xml", "include/xdg-shell-server-protocol.h"),
        ("private-code", "/usr/share/wayland-protocols/stable/xdg-shell/xdg-shell.xml", "xdg-shell-protocol.c"),
        ("server-header", "protocol/wayland-drm.xml", "include/wayland-drm-server-protocol.h"),
        ("server-header", "/usr/share/wayland-protocols/unstable/linux-dmabuf/linux-dmabuf-unstable-v1.xml", "include/linux-dmabuf-unstable-v1-server-protocol.h"),
        ("server-header", "/usr/share/wayland-protocols/unstable/xdg-decoration/xdg-decoration-unstable-v1.xml", "include/xdg-decoration-unstable-v1-server-protocol.h"),
    ]
    for kind, src, out in cmds:
        self.do("wayland-scanner", kind, src, out)
    self.do(
        "wayland-scanner", "private-code",
        "/usr/share/wayland-protocols/unstable/xdg-decoration/xdg-decoration-unstable-v1.xml",
        "xdg-decoration-unstable-v1-protocol.c",
    )
    self.do(
        "wayland-scanner", "private-code",
        "/usr/share/wayland-protocols/unstable/linux-dmabuf/linux-dmabuf-unstable-v1.xml",
        "linux-dmabuf-unstable-v1-protocol.c",
    )


def build(self):
    from cbuild.util import compiler

    cc = compiler.C(self)
    self.mkdir("obj", parents=True)

    cc.invoke(["cursor/convert_font.c"], "convert_font", flags=["-std=gnu99", "-Wall"])
    self.do("./convert_font", "cursor/cursor.pcf", "cursor/cursor_data.h")

    objs = []
    for src in _lib_sources:
        obj = "obj/" + src.replace("/", "_").removesuffix(".c") + ".o"
        cc.invoke([src], obj, obj_file=True, flags=_cflags)
        objs.append(obj)

    for src, obj in [
        ("launch/protocol.c", "obj/launch_protocol.o"),
        ("server-decoration-protocol.c", "obj/server-decoration-protocol.o"),
        ("swc-protocol.c", "obj/swc-protocol.o"),
        ("xdg-shell-protocol.c", "obj/xdg-shell-protocol.o"),
        ("xdg-decoration-unstable-v1-protocol.c", "obj/xdg-decoration-protocol.o"),
        ("linux-dmabuf-unstable-v1-protocol.c", "obj/linux-dmabuf-protocol.o"),
    ]:
        cc.invoke([src], obj, obj_file=True, flags=_cflags)
        objs.append(obj)
    self.do("ar", "rcs", "libswc.a", *objs)

    cc.invoke(
        ["launch/launch.c", "launch/devmajor-linux.c", "obj/launch_protocol.o"],
        "swc-launch",
        flags=_cflags,
        ldflags=[
            "-static-pie",
            "/usr/lib/libdrm.a",
            "/usr/lib/libudev.a",
            "-lz",
            "-lm",
            "-ldl",
            "-lpthread",
            "-lrt",
        ],
    )


def post_build(self):
    # mirror the Oasis lua recipe: libswc.a embeds the Oasis stack so velox
    # only has to link libswc.a and the Wayland server library
    self.do(
        "sh",
        "-c",
        "printf 'create libswc-merged.a\\n"
        "addlib libswc.a\\n"
        "addlib /usr/lib/libinput.a\\n"
        "addlib /usr/lib/libquirks.a\\n"
        "addlib /usr/lib/liblibinput-util.a\\n"
        "addlib /usr/lib/liblibinput-util-libinput.a\\n"
        "addlib /usr/lib/libxkbcommon.a\\n"
        "addlib /usr/lib/libwayland-server.a\\n"
        "addlib /usr/lib/libwld.a\\n"
        "addlib /usr/lib/libevdev.a\\n"
        "addlib /usr/lib/libmtdev.a\\n"
        "addlib /usr/lib/libudev.a\\n"
        "addlib /usr/lib/libdrm.a\\n"
        "addlib /usr/lib/libpixman-1.a\\n"
        "addlib /usr/lib/libfontconfig.a\\n"
        "addlib /usr/lib/libfreetype.a\\n"
        "addlib /usr/lib/libexpat.a\\n"
        "addlib /usr/lib/libffi.a\\n"
        "addlib /usr/lib/libxml2.a\\n"
        "addlib /usr/lib/libz.a\\n"
        "save\\nend\\n' | ar -M && mv libswc-merged.a libswc.a",
    )


def install(self):
    self.install_bin("swc-launch")
    self.install_lib("libswc.a", mode=0o644)
    for h in ("swc.h",):
        self.install_file(f"libswc/{h}", "usr/include")
    for h in (
        "swc-client-protocol.h",
        "swc-server-protocol.h",
        "server-decoration-server-protocol.h",
        "xdg-shell-server-protocol.h",
        "wayland-drm-server-protocol.h",
    ):
        self.install_file(f"include/{h}", "usr/include")
    self.install_file("swc-protocol.c", "usr/share/swc")
    self.install_file("protocol/swc.xml", "usr/share/swc")
    self.install_license("LICENSE")


@subpackage("swc-devel")
def _(self):
    return ["usr/include", "usr/share/swc"]
