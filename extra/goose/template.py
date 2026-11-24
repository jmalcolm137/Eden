pkgname = "goose"
pkgver = "2026.4"
pkgrel = 1
build_style = "cmake"
configure_args = [
    "-DCMAKE_BUILD_TYPE=Release",
    "-DGOOSE_BUILTIN_LIBS=",
    "-DGOOSE_STDLIB_PATH=/usr/share/goose/stdlib",
    "-DGOOSE_TCC_LIB_PATH=/usr/lib/goose/tcclib",
    f"-DGOOSE_VERSION=v{pkgver}",
]
hostmakedepends = ["cmake", "ninja", "pkgconf"]
pkgdesc = "Memory-safe systems programming language without a heap"
license = "Apache-2.0"
url = "https://aardappel.github.io/goose"
source = f"https://github.com/aardappel/goose/archive/refs/tags/v{pkgver}.tar.gz"
sha256 = "943d785fb191de7b52539e9cf16715701babcacd339323f786729c2132343d9b"
# tests need a full toolchain and build environment
options = ["!check", "!lto"]


def install(self):
    self.install_bin(self.cwd / "build/goose")
    # the compiler locates its standard library and TinyCC runtime here
    self.install_files(self.cwd / "stdlib", "usr/share/goose")
    self.install_files(self.cwd / "build/tcclib", "usr/lib/goose")
    self.install_license("LICENSE")
