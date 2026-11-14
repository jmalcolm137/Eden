pkgname = "libplacebo"
pkgver = "7.349.0"
pkgrel = 0
# Oasis pkg/libplacebo/src
_commit = "1fd3c7bde7b943fe8985c893310b5269a09b46c5"
pkgdesc = "Reusable library for GPU-accelerated video/image rendering"
license = "LGPL-2.1-or-later"
url = "https://code.videolan.org/videolan/libplacebo"
source = f"{url}/-/archive/{_commit}/libplacebo-{_commit}.tar.gz"
sha256 = "067cd40a3f7ff78d03eeb15665db15e8de45c02423c16a4af07e3c79864f2415"
# static-only library, as in the Oasis recipe
options = ["!lto", "!check"]

_cflags = ["-std=c11", "-Wall", "-D_XOPEN_SOURCE=700", "-I.", "-Isrc", "-Isrc/include", "-Iinclude"]

_headers = [
    "cache.h", "colorspace.h", "common.h", "d3d11.h", "dispatch.h",
    "dither.h", "dummy.h", "filters.h", "gamut_mapping.h", "gpu.h",
    "log.h", "opengl.h", "options.h", "renderer.h", "swapchain.h",
    "tone_mapping.h", "vulkan.h", "shaders.h",
    "shaders/colorspace.h", "shaders/custom.h", "shaders/deinterlacing.h",
    "shaders/dithering.h", "shaders/film_grain.h", "shaders/icc.h",
    "shaders/lut.h", "shaders/sampling.h",
    "utils/dav1d.h", "utils/dav1d_internal.h", "utils/dolbyvision.h",
    "utils/frame_queue.h", "utils/libav.h", "utils/libav_internal.h",
    "utils/upload.h",
]


def pre_build(self):
    self.cp(self.files_path / "config_internal.h", "config_internal.h")
    self.mkdir("include/libplacebo", parents=True)
    src = (self.cwd / "src/include/libplacebo/config.h.in").read_text()
    src = src.replace("@majorver@", "7").replace("@apiver@", "349")
    src = "\n".join(line for line in src.splitlines() if "@extra_defs@" not in line) + "\n"
    (self.cwd / "include/libplacebo/config.h").write_text(src)
    (self.cwd / "version.h").write_text('#define BUILD_VERSION "7.349.0"\n')


def build(self):
    from cbuild.util import compiler

    cc = compiler.C(self)
    self.mkdir("obj", parents=True)
    objs = []
    for src in ("src/colorspace.c", "src/common.c"):
        obj = "obj/" + src.replace("/", "_").removesuffix(".c") + ".o"
        cc.invoke([src], obj, obj_file=True, flags=_cflags)
        objs.append(obj)
    self.do("ar", "rcs", "libplacebo.a", *objs)


def install(self):
    self.install_lib("libplacebo.a", mode=0o644)
    for h in _headers:
        dest = "usr/include/libplacebo"
        if "/" in h:
            dest += "/" + h.rsplit("/", 1)[0]
        self.install_file(f"src/include/libplacebo/{h}", dest)
    self.install_file("include/libplacebo/config.h", "usr/include/libplacebo")
    self.install_file("version.h", "usr/include/libplacebo")
    self.install_license("LICENSE")


@subpackage("libplacebo-devel")
def _(self):
    return ["usr/include"]
