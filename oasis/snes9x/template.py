pkgname = "snes9x"
pkgver = "0_git20200101"
pkgrel = 0
# Oasis pkg/snes9x/src (libretro core)
_commit = "32e556249e39ecd9fbff7ef1d1297ffa152cbbe1"
pkgdesc = "Super Nintendo emulator libretro core"
license = "custom:snes9x"
url = "https://github.com/libretro/snes9x2010"
source = f"https://github.com/libretro/snes9x2010/archive/{_commit}.tar.gz"
sha256 = "077dc8bceab4586be7736bb3405e41648dd144d055c4074157c3cf985f53963c"
# no test suite in the Oasis recipe
options = ["!distlicense", "!check"]

_cflags = [
    "-std=c99", "-Wall", "-Wpedantic", "-Wno-format-truncation",
    "-D_DEFAULT_SOURCE", "-D__LIBRETRO__", "-DRIGHTSHIFT_IS_SAR", "-DLAGFIX",
    "-fPIC", "-Ilibretro/libretro-common/include",
]


def build(self):
    from cbuild.util import compiler

    cc = compiler.C(self)
    sources = sorted(
        str(p.relative_to(self.cwd))
        for p in (self.cwd / "src").glob("*.c")
        if p.name != "snes9x_griffin.c"
    )
    sources += [
        "filter/snes_ntsc.c",
        "libretro/libretro.c",
        "libretro/libretro-common/streams/memory_stream.c",
    ]
    self.mkdir("out", parents=True)
    cc.invoke(
        sources,
        "out/snes9x_libretro.so",
        flags=_cflags,
        ldflags=["-shared"],
    )


def install(self):
    self.install_dir("usr/lib/libretro")
    self.install_file("out/snes9x_libretro.so", "usr/lib/libretro", mode=0o755)
    self.install_license(self.files_path / "LICENSE.txt")
