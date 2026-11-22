pkgname = "oniguruma"
pkgver = "6.9.10"
pkgrel = 0
archs = ["x86_64"]
build_style = "cmake"
configure_args = ["-DBUILD_SHARED_LIBS=ON"]
hostmakedepends = ["cmake", "pkgconf", "samurai"]
pkgdesc = "Regular expression library"
license = "BSD-2-Clause"
url = "https://github.com/kkos/oniguruma"
source = f"https://github.com/kkos/oniguruma/archive/refs/tags/v{pkgver}.tar.gz"
sha256 = "ad92309d0d13eebc27f6592e875f3efbfa3dda2bf6da5952e00f0a2120c921a8"
# the test suite needs the full autotools test harness
options = ["!check"]


@subpackage("oniguruma-devel")
def _(self):
    return self.default_devel()


def post_install(self):
    self.install_license("COPYING")
