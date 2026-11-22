pkgname = "libjpeg-turbo"
pkgver = "3.2.1"
pkgrel = 1
archs = ["x86_64"]
build_style = "cmake"
configure_args = [
    "-DENABLE_SHARED=ON",
    "-DENABLE_STATIC=OFF",
    "-DWITH_JPEG8=ON",
    "-DWITH_JAVA=OFF",
    "-DWITH_TESTS=OFF",
    "-DWITH_TOOLS=ON",
    "-DWITH_TURBOJPEG=ON",
]
hostmakedepends = ["cmake", "nasm", "pkgconf", "samurai"]
pkgdesc = "JPEG image codec with SIMD acceleration"
license = "IJG AND BSD-3-Clause AND Zlib"
url = "https://libjpeg-turbo.org"
source = f"https://github.com/libjpeg-turbo/libjpeg-turbo/archive/refs/tags/{pkgver}.tar.gz"
sha256 = "6f5819c51649bce2571a23b1b0cd41eae2f57fc3f8908c7ec9e7047efb65ca13"
# needs the upstream regression test harness
options = ["!check"]


@subpackage("libjpeg-turbo-devel")
def _(self):
    return self.default_devel()


@subpackage("libjpeg-turbo-progs")
def _(self):
    return self.default_progs()


def post_install(self):
    self.install_license("LICENSE.md")
