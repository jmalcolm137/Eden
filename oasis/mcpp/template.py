pkgname = "mcpp"
pkgver = "2.7.2"
pkgrel = 2
build_style = "gnu_configure"
configure_args = ["--disable-static"]
configure_gen = []
makedepends = [
    "libatomic-chimera-devel-static",
    "libunwind-devel-static",
    "musl-devel-static",
]
pkgdesc = "Portable C preprocessor"
license = "BSD-2-Clause"
url = "http://mcpp.sourceforge.net"
source = f"https://downloads.sourceforge.net/{pkgname}/{pkgname}-{pkgver}.tar.gz"
sha256 = "3b9b4421888519876c4fc68ade324a3bbd81ceeb7092ecdbbc2055099fcb8864"
# the 2008 sources rely on old-style pointer conversions
tool_flags = {
    "CFLAGS": ["-Wno-incompatible-pointer-types"],
    # self-contained executable, no dynamic loader
    "LDFLAGS": ["-static-pie"],
}
# no test suite
options = ["!check"]


@subpackage("mcpp-doc")
def _(self):
    return self.default_doc()


def post_install(self):
    self.install_license("LICENSE")
