pkgname = "freetype"
pkgver = "2.11.0"
pkgrel = 0
# Oasis pkg/freetype/src
_commit = "801cd842e27c85cb1d5000f6397f382ffe295daa"
makedepends = ["zlib-static"]
pkgdesc = "Font rendering library from Oasis"
license = "FTL OR GPL-2.0-or-later"
url = "https://freetype.org"
source = f"https://github.com/freetype/freetype/archive/{_commit}.tar.gz"
sha256 = "644c4eb98677385b70412af59c03f5504587d5ce02387b1bcaac12abe1aadbc7"
# no test suite
options = ["!check", "!lto"]

_sources = [
    "builds/unix/ftsystem.c",
    "src/base/ftdebug.c", "src/base/ftinit.c", "src/base/ftbase.c",
    "src/base/ftbbox.c", "src/base/ftbdf.c", "src/base/ftbitmap.c",
    "src/base/ftcid.c", "src/base/ftfstype.c", "src/base/ftgasp.c",
    "src/base/ftglyph.c", "src/base/ftgxval.c", "src/base/ftmm.c",
    "src/base/ftotval.c", "src/base/ftpatent.c", "src/base/ftpfr.c",
    "src/base/ftstroke.c", "src/base/ftsynth.c", "src/base/fttype1.c",
    "src/base/ftwinfnt.c",
    "src/truetype/truetype.c",
    "src/type1/type1.c",
    "src/cff/cff.c",
    "src/cid/type1cid.c",
    "src/pfr/pfr.c",
    "src/type42/type42.c",
    "src/winfonts/winfnt.c",
    "src/pcf/pcf.c",
    "src/bdf/bdf.c",
    "src/sfnt/sfnt.c",
    "src/autofit/autofit.c",
    "src/pshinter/pshinter.c",
    "src/smooth/smooth.c",
    "src/raster/raster.c",
    "src/sdf/sdf.c",
    "src/cache/ftcache.c",
    "src/gzip/ftgzip.c",
    "src/lzw/ftlzw.c",
    "src/bzip2/ftbzip2.c",
    "src/psaux/psaux.c",
    "src/psnames/psnames.c",
]


def build(self):
    from cbuild.util import compiler

    cc = compiler.C(self)
    objs = []
    flags = [
        "-std=c99",
        "-Wall",
        "-Wpedantic",
        "-DFT2_BUILD_LIBRARY",
        "-DFT_CONFIG_OPTION_SYSTEM_ZLIB",
        "-DHAVE_FCNTL_H",
        "-DHAVE_UNISTD_H",
        "-Ibuilds/unix",
        "-Iinclude",
        "-Iinclude/freetype/config",
    ]
    self.mkdir("obj", parents=True)

    for src in _sources:
        obj = "obj/" + src.replace("/", "_").removesuffix(".c") + ".o"
        cc.invoke([src], obj, obj_file=True, flags=flags)
        objs.append(obj)

    self.do("ar", "rcs", "libfreetype.a", *objs)


def install(self):
    self.install_file("libfreetype.a", "usr/lib")
    self.install_file("include/ft2build.h", "usr/include")
    for src in sorted((self.cwd / "include/freetype").rglob("*.h")):
        rel = src.relative_to(self.cwd / "include")
        dest = "usr/include"
        if str(rel.parent) != ".":
            dest += f"/{rel.parent}"
        self.install_file(f"include/{rel}", dest)
    self.install_license("LICENSE.TXT")
