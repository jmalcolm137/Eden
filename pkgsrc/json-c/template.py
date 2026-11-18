pkgname = "json-c"
pkgver = "0.18"
pkgrel = 1
build_style = "cmake"
configure_args = [
    "-DBUILD_SHARED_LIBS=ON",
    "-DBUILD_STATIC_LIBS=OFF",
    "-DBUILD_TESTING=OFF",
    "-DDISABLE_WERROR=ON",
]
hostmakedepends = ["cmake", "ninja", "pkgconf"]
pkgdesc = "JSON implementation in C"
license = "MIT"
url = "https://github.com/json-c/json-c"
source = f"https://s3.amazonaws.com/json-c_releases/releases/json-c-{pkgver}.tar.gz"
sha256 = "876ab046479166b869afc6896d288183bbc0e5843f141200c677b3e8dfb11724"
# tests are not built
options = ["!check"]


@subpackage("json-c-devel")
def _(self):
    return self.default_devel()


def post_install(self):
    self.install_license("COPYING")


def post_patch(self):
    # CMake 4 no longer accepts compatibility with pre-3.5 projects
    p = self.cwd / "apps/CMakeLists.txt"
    p.write_text(p.read_text().replace("cmake_minimum_required(VERSION 2.8)", "cmake_minimum_required(VERSION 3.9)"))
