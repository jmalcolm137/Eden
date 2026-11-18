pkgname = "libpng"
pkgver = "1.6.59"
pkgrel = 1
build_style = "gnu_configure"
configure_args = ["--disable-riscv-rvv"]
configure_gen = []
hostmakedepends = ["pkgconf"]
makedepends = [
    "libatomic-chimera-devel-static",
    "libunwind-devel-static",
    "musl-devel-static",
    "zlib-static",
]
pkgdesc = "Library for manipulating PNG images"
license = "Libpng"
url = "https://www.libpng.org/pub/png/libpng.html"
source = "https://downloads.sourceforge.net/sourceforge/libpng/libpng-1.6.59.tar.xz"
sha256 = "d80dd2a38a37f803cb9b6ac7b14bd6e74ddc3b654780a8380bdf93523fdb4389"
# tests need test images and a display
options = ["!check", "!splitstatic"]


def post_build(self):
    # Keep libpng16.so for consumers; relink the bundled tools statically.
    from cbuild.util import compiler

    cc = compiler.C(self)
    flags = ["-DHAVE_CONFIG_H", "-I.", "-Ibuild", "-Icontrib/tools"]
    for src, out in [
        ("contrib/tools/pngfix.c", "pngfix-static"),
        ("contrib/tools/png-fix-itxt.c", "png-fix-itxt-static"),
    ]:
        cc.invoke(
            [src],
            out,
            flags=flags,
            ldflags=["build/.libs/libpng16.a", "-lz", "-lm", "-static-pie"],
        )


def post_install(self):
    self.install_license("LICENSE")
    for name in ["pngfix", "png-fix-itxt"]:
        self.uninstall(f"usr/bin/{name}", missing_ok=True)
        self.install_bin(f"{name}-static", name=name)


@subpackage("libpng-devel")
def _(self):
    return self.default_devel()
