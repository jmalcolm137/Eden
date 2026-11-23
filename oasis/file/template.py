pkgname = "file"
pkgver = "5.45"
pkgrel = 1
build_style = "gnu_configure"
configure_args = [
    "--disable-bzlib",
    "--disable-xzlib",
    "--disable-lzlib",
]
configure_gen = []
makedepends = [
    "libatomic-chimera-devel-static",
    "libunwind-devel-static",
    "musl-devel-static",
    "zlib",
]
pkgdesc = "File type identification utility"
license = "BSD-2-Clause"
url = "https://www.darwinsys.com/file"
source = f"https://astron.com/pub/file/file-{pkgver}.tar.gz"
sha256 = "fc97f51029bb0e2c9f4e3bffefdaf678f0e039ee872b9de5c002a6d09c784d82"
# no test suite in the Oasis recipe
options = ["!check"]


@subpackage("file-devel")
def _(self):
    return self.default_devel()


def post_build(self):
    # The default build links src/file against libmagic.so; relink it
    # statically while still shipping the shared libmagic for consumers.
    from cbuild.util import compiler

    # The libtool build does not leave a static libmagic archive behind, so
    # fold the PIC objects into one for the static relink.
    objs = [
        str(p.relative_to(self.cwd))
        for p in sorted((self.cwd / "build/src/.libs").glob("*.o"))
        if p.name != "file.o"
    ]
    self.do("ar", "rcs", "libmagic.a", *objs)

    cc = compiler.C(self)
    cc.invoke(
        ["src/file.c"],
        "file-static",
        flags=["-DHAVE_CONFIG_H", "-I.", "-Isrc", "-Ibuild", "-Ibuild/src"],
        ldflags=["libmagic.a", "-lz", "-lm", "-static-pie"],
    )


def post_install(self):
    self.install_license("COPYING")
    self.uninstall("usr/bin/file")
    self.install_bin("file-static", name="file")
