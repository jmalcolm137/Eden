pkgname = "brotli"
pkgver = "1.2.1"
pkgrel = 0
build_style = "cmake"
configure_args = [
    "-DBROTLI_DISABLE_TESTS=ON",
    "-DBUILD_SHARED_LIBS=ON",
]
hostmakedepends = ["cmake", "ninja", "pkgconf"]
pkgdesc = "Brotli compression library"
license = "MIT"
url = "https://github.com/google/brotli"
source = f"https://github.com/google/brotli/archive/refs/tags/v{pkgver}.tar.gz"
sha256 = "98d35d11a78dc453aebb7d10c3748f3f73ff78c8267c0dc697b8631f67bf7e8f"
# tests are not built
options = ["!check"]


@subpackage("brotli-devel")
def _(self):
    return self.default_devel()


@subpackage("brotli-progs")
def _(self):
    return self.default_progs()


def post_install(self):
    self.install_license("LICENSE")
