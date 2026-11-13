pkgname = "libcbor"
pkgver = "0.9.0"
pkgrel = 0
# Oasis pkg/libcbor/src
_commit = "58b3319b8c3ec15171cb00f01a3a1e9d400899e1"
build_style = "cmake"
configure_args = [
    "-DBUILD_SHARED_LIBS=OFF",
    "-DWITH_TESTS=OFF",
    "-DWITH_EXAMPLES=OFF",
]
hostmakedepends = ["cmake"]
pkgdesc = "CBOR serialization library"
license = "MIT"
url = "https://github.com/PJK/libcbor"
source = f"{url}/archive/{_commit}.tar.gz"
sha256 = "6df64c580ddd91567d01055586a66db3d61fe31c7c17f12b4ba7232eb75c80e2"
# no test suite in the Oasis recipe
options = ["!lto", "!check"]


@subpackage("libcbor-devel")
def _(self):
    return ["usr/include", "usr/lib/pkgconfig"]



def post_install(self):
    self.install_license("LICENSE.md")
