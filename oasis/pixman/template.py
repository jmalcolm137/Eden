pkgname = "pixman"
pkgver = "0.40.0"
pkgrel = 0
# Oasis pkg/pixman/src
_commit = "e8df10eea9609609568bf4cbc05796594c1b978d"
pkgdesc = "Low-level pixel manipulation library from Oasis"
license = "MIT"
url = "https://pixman.org"
source = (
    "https://gitlab.freedesktop.org/pixman/pixman/-/archive/"
    f"{_commit}/pixman-{_commit}.tar.gz"
)
sha256 = "c1167b71b3685c8874b9de06319891d9910f84cec0846b3d3b77caed27fb2c95"
# no test suite
options = ["!check", "!lto"]

_sources = [
    "pixman/pixman.c",
    "pixman/pixman-access.c",
    "pixman/pixman-access-accessors.c",
    "pixman/pixman-bits-image.c",
    "pixman/pixman-combine32.c",
    "pixman/pixman-combine-float.c",
    "pixman/pixman-conical-gradient.c",
    "pixman/pixman-filter.c",
    "pixman/pixman-x86.c",
    "pixman/pixman-mips.c",
    "pixman/pixman-arm.c",
    "pixman/pixman-ppc.c",
    "pixman/pixman-edge.c",
    "pixman/pixman-edge-accessors.c",
    "pixman/pixman-fast-path.c",
    "pixman/pixman-glyph.c",
    "pixman/pixman-general.c",
    "pixman/pixman-gradient-walker.c",
    "pixman/pixman-image.c",
    "pixman/pixman-implementation.c",
    "pixman/pixman-linear-gradient.c",
    "pixman/pixman-matrix.c",
    "pixman/pixman-noop.c",
    "pixman/pixman-radial-gradient.c",
    "pixman/pixman-region16.c",
    "pixman/pixman-region32.c",
    "pixman/pixman-solid-fill.c",
    "pixman/pixman-timer.c",
    "pixman/pixman-trap.c",
    "pixman/pixman-utils.c",
]

_x86_sources = [
    "pixman/pixman-mmx.c",
    "pixman/pixman-sse2.c",
    "pixman/pixman-ssse3.c",
]


def pre_build(self):
    self.cp(self.files_path / "config.h", "config.h")
    self.cp(self.files_path / "pixman.patch", "pixman.patch")
    self.do("patch", "-p1", "-i", "pixman.patch")

    text = (self.cwd / "pixman/pixman-version.h.in").read_text()
    text = text.replace("@PIXMAN_VERSION_MAJOR@", "0")
    text = text.replace("@PIXMAN_VERSION_MINOR@", "40")
    text = text.replace("@PIXMAN_VERSION_MICRO@", "0")
    (self.cwd / "pixman-version.h").write_text(text)


def build(self):
    from cbuild.util import compiler

    cc = compiler.C(self)
    objs = []
    flags = [
        "-DHAVE_CONFIG_H",
        "-I.",
        "-DHAVE__THREAD_LOCAL=1",
        "-DHAVE___BUILTIN_CLZ=1",
    ]
    self.mkdir("obj", parents=True)

    for src in _sources:
        obj = "obj/" + src.rsplit("/", 1)[-1].removesuffix(".c") + ".o"
        cc.invoke([src], obj, obj_file=True, flags=flags)
        objs.append(obj)

    if self.profile.arch == "x86_64":
        for src, extra in [
            (_x86_sources[0], ["-mmmx"]),
            (_x86_sources[1], ["-msse2"]),
            (_x86_sources[2], ["-mssse3"]),
        ]:
            obj = "obj/" + src.rsplit("/", 1)[-1].removesuffix(".c") + ".o"
            cc.invoke([src], obj, obj_file=True, flags=flags + extra)
            objs.append(obj)

    self.do("ar", "rcs", "libpixman.a", *objs)


def install(self):
    self.install_file("libpixman.a", "usr/lib")
    self.install_file("pixman/pixman.h", "usr/include")
    self.install_file("pixman-version.h", "usr/include")
    self.install_license("COPYING")
