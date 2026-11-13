pkgname = "pcre"
pkgver = "8.45"
pkgrel = 0
build_style = "gnu_configure"
configure_args = [
    "--disable-cpp",
    "--disable-pcre16",
    "--disable-pcre32",
    "--enable-utf",
    "--enable-unicode-properties",
    "--enable-jit",
    "--disable-shared",
    "--enable-static",
]
configure_gen = []
pkgdesc = "Perl-compatible regular expression library"
license = "BSD-3-Clause"
url = "https://www.pcre.org"
source = (
    "https://sourceforge.net/projects/pcre/files/pcre/8.45/"
    "pcre-8.45.tar.gz/download>pcre-8.45.tar.gz"
)
sha256 = "4e6ce03e0336e8b4a3d6c2b70b1c5e18590a5673a98186da90d4f33c23defc09"
# no test suite in the Oasis recipe
options = ["!check"]


@subpackage("pcre-devel")
def _(self):
    return ["usr/include", "usr/lib/pkgconfig"]


@subpackage("pcre-devel-static")
def _(self):
    return ["usr/lib/*.a"]


def post_install(self):
    self.install_license("LICENCE")
