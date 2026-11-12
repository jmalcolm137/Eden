pkgname = "bearssl"
pkgver = "0.6"
pkgrel = 0
build_style = "makefile"
make_build_args = ["build/libbearssl.a", "build/libbearssl.so"]
pkgdesc = "BearSSL TLS and crypto library"
license = "MIT"
url = "https://bearssl.org"
source = f"https://bearssl.org/bearssl-{pkgver}.tar.gz"
sha256 = "6705bba1714961b41a728dfc5debbe348d2966c117649392f8c8139efc83ff14"
tool_flags = {"CFLAGS": ["-fPIC"]}
# no tests; upstream's make only builds the library and tools
options = ["!check"]


def install(self):
    self.install_dir("usr/lib")
    self.install_file(self.cwd / "build/libbearssl.so", "usr/lib")
    self.install_file(self.cwd / "build/libbearssl.a", "usr/lib")
    self.install_dir("usr/include")
    for h in (self.cwd / "inc").glob("*.h"):
        self.install_file(h, "usr/include")
    self.install_license("LICENSE.txt")


@subpackage("bearssl-devel")
def _(self):
    return ["usr/include"]


@subpackage("bearssl-devel-static")
def _(self):
    return ["usr/lib/*.a"]
