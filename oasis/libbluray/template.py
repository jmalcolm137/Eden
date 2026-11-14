pkgname = "libbluray"
pkgver = "1.3.4"
pkgrel = 0
makedepends = ["freetype"]
pkgdesc = "Blu-ray disc playback library"
license = "LGPL-2.1-or-later"
url = "https://www.videolan.org/developers/libbluray.html"
source = f"https://download.videolan.org/pub/videolan/libbluray/{pkgver}/libbluray-{pkgver}.tar.bz2"
sha256 = "478ffd68a0f5dde8ef6ca989b7f035b5a0a22c599142e5cd3ff7b03bbebe5f2b"
# static-only library, as in the Oasis recipe
options = ["!lto", "!check"]

_cflags = [
    "-std=c99", "-Wall", "-Wpedantic", "-Wno-error", "-DHAVE_CONFIG_H", "-D_GNU_SOURCE",
    "-I.", "-Isrc", "-Isrc/libbluray", "-Ijni", "-Ijni/linux",
    "-Icontrib/libudfread/src", "-Iinclude",
]

_sources = [
    "src/file/file.c", "src/file/filesystem.c", "src/libbluray/bluray.c",
    "src/libbluray/register.c", "src/libbluray/bdnav/bdid_parse.c",
    "src/libbluray/bdnav/bdmv_parse.c", "src/libbluray/bdnav/clpi_parse.c",
    "src/libbluray/bdnav/extdata_parse.c", "src/libbluray/bdnav/index_parse.c",
    "src/libbluray/bdnav/meta_parse.c", "src/libbluray/bdnav/mpls_parse.c",
    "src/libbluray/bdnav/navigation.c", "src/libbluray/bdnav/sound_parse.c",
    "src/libbluray/bdnav/uo_mask.c", "src/libbluray/decoders/graphics_controller.c",
    "src/libbluray/decoders/graphics_processor.c", "src/libbluray/decoders/ig_decode.c",
    "src/libbluray/decoders/m2ts_demux.c", "src/libbluray/decoders/m2ts_filter.c",
    "src/libbluray/decoders/pg_decode.c", "src/libbluray/decoders/pes_buffer.c",
    "src/libbluray/decoders/rle.c", "src/libbluray/decoders/textst_decode.c",
    "src/libbluray/decoders/textst_render.c", "src/libbluray/disc/aacs.c",
    "src/libbluray/disc/bdplus.c", "src/libbluray/disc/dec.c",
    "src/libbluray/disc/disc.c", "src/libbluray/disc/properties.c",
    "src/libbluray/hdmv/hdmv_vm.c", "src/libbluray/hdmv/mobj_parse.c",
    "src/libbluray/hdmv/mobj_print.c", "src/util/array.c", "src/util/bits.c",
    "src/util/event_queue.c", "src/util/logging.c", "src/util/mutex.c",
    "src/util/refcnt.c", "src/util/strutl.c", "src/util/time.c",
    "src/libbluray/bdj/bdj.c", "src/libbluray/bdj/bdjo_parse.c",
    "src/libbluray/bdj/native/bdjo.c",
    "src/libbluray/bdj/native/java_awt_BDFontMetrics.c",
    "src/libbluray/bdj/native/java_awt_BDGraphics.c",
    "src/libbluray/bdj/native/org_videolan_Libbluray.c",
    "src/libbluray/bdj/native/org_videolan_Logger.c",
    "src/libbluray/bdj/native/register_native.c",
    "src/libbluray/bdj/native/util.c", "src/libbluray/disc/udf_fs.c",
    "contrib/libudfread/src/default_blockinput.c",
    "contrib/libudfread/src/ecma167.c", "contrib/libudfread/src/udfread.c",
    "src/file/dir_posix.c", "src/file/dirs_xdg.c", "src/file/dl_posix.c",
    "src/file/file_posix.c", "src/file/mount.c",
]

_headers = [
    "src/libbluray/bluray.h", "src/libbluray/keys.h",
    "src/util/log_control.h", "src/libbluray/bdnav/meta_data.h",
    "src/libbluray/decoders/overlay.h",
]


def pre_build(self):
    self.cp(self.files_path / "config.h", "config.h")
    self.mkdir("include/libbluray", parents=True)
    text = (self.cwd / "src/libbluray/bluray-version.h.in").read_text()
    text = text.replace("@BLURAY_VERSION_MAJOR@", "1")
    text = text.replace("@BLURAY_VERSION_MINOR@", "3")
    text = text.replace("@BLURAY_VERSION_MICRO@", "4")
    (self.cwd / "include/libbluray/bluray-version.h").write_text(text)


def build(self):
    from cbuild.util import compiler

    cc = compiler.C(self)
    self.mkdir("obj", parents=True)
    objs = []
    for src in _sources:
        obj = "obj/" + src.replace("/", "_").removesuffix(".c") + ".o"
        cc.invoke([src], obj, obj_file=True, flags=_cflags)
        objs.append(obj)
    self.do("ar", "rcs", "libbluray.a", *objs)


def install(self):
    self.install_lib("libbluray.a", mode=0o644)
    for h in _headers:
        self.install_file(h, "usr/include/libbluray")
    self.install_file("include/libbluray/bluray-version.h", "usr/include/libbluray")
    self.install_license("COPYING")


@subpackage("libbluray-devel")
def _(self):
    return ["usr/include"]
