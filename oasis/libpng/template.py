pkgname = "libpng"
pkgver = "1.6.43"
pkgrel = 1
# Oasis pkg/libpng/src
_commit = "ed217e3e601d8e462f7fd1e04bed43ac42212429"
makedepends = ["zlib-static"]
pkgdesc = "PNG image library from Oasis"
license = "Libpng"
url = "https://www.libpng.org/pub/png/libpng.html"
source = f"https://github.com/glennrp/libpng/archive/{_commit}.tar.gz"
sha256 = "3179215477e554acc3630b8a508488ade049a359c75253e377e136add1252c9d"
# no test suite
options = ["!check", "!lto"]

_sources = [
    "png.c", "pngerror.c", "pngget.c", "pngmem.c", "pngpread.c",
    "pngread.c", "pngrio.c", "pngrtran.c", "pngrutil.c", "pngset.c",
    "pngtrans.c", "pngwio.c", "pngwrite.c", "pngwtran.c", "pngwutil.c",
]


def pre_build(self):
    self.cp(self.files_path / "config.h", "config.h")
    self.cp(self.files_path / "libpng.patch", "libpng.patch")
    self.do("patch", "-p1", "-i", "libpng.patch")

    with open(self.cwd / "pnglibconf.tf4", "w") as f:
        self.do(
            "awk", "-f", "scripts/options.awk", "out=/dev/stdout",
            "version=search", "pngconf.h", "scripts/pnglibconf.dfa",
            "pngusr.dfa",
            stdout=f,
        )
    with open(self.cwd / "pnglibconf.c", "w") as f:
        self.do(
            "awk", "-f", "scripts/options.awk", "out=/dev/stdout",
            "pnglibconf.tf4",
            stdout=f,
        )
    with open(self.cwd / "pnglibconf.tf1", "w") as f:
        self.do("clang-cpp", "pnglibconf.c", stdout=f)
    with open(self.cwd / "pnglibconf.h", "w") as f:
        self.do(
            "awk", "-f", "scripts/dfn.awk", "out=/dev/stdout",
            "pnglibconf.tf1",
            stdout=f,
        )


def build(self):
    from cbuild.util import compiler

    cc = compiler.C(self)
    objs = []
    flags = ["-DHAVE_CONFIG_H", "-I.", "-I/usr/include"]
    self.mkdir("obj", parents=True)

    for src in _sources:
        obj = "obj/" + src.removesuffix(".c") + ".o"
        cc.invoke([src], obj, obj_file=True, flags=flags)
        objs.append(obj)

    self.do("ar", "rcs", "libpng.a", *objs)


def install(self):
    self.install_file("libpng.a", "usr/lib")
    self.install_file("png.h", "usr/include")
    self.install_file("pngconf.h", "usr/include")
    self.install_file("pnglibconf.h", "usr/include")
    self.install_license("LICENSE")
