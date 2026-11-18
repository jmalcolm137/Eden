# header files only
pkgname = "fast_float"
pkgver = "8.1.0"
pkgrel = 0
build_style = "cmake"
configure_args = [
    "-DFASTFLOAT_BENCHMARKS=OFF",
    "-DFASTFLOAT_INSTALL=ON",
    "-DFASTFLOAT_SANITIZE=OFF",
    "-DFASTFLOAT_TEST=OFF",
]
hostmakedepends = ["cmake", "ninja", "pkgconf"]
pkgdesc = "Fast float parsing library"
license = "Apache-2.0 OR MIT"
url = "https://github.com/fastfloat/fast_float"
source = f"https://github.com/fastfloat/fast_float/archive/refs/tags/v{pkgver}.tar.gz"
sha256 = "4bfabb5979716995090ce68dce83f88f99629bc17ae280eae79311c5340143e1"
# header-only, no tests
options = ["!check", "!strip", "!splitstatic"]


def post_install(self):
    self.install_license("LICENSE-APACHE")
    self.install_license("LICENSE-MIT")
