pkgname = "libtirpc"
pkgver = "1.3.7"
pkgrel = 0
build_style = "gnu_configure"
configure_args = ["--disable-gssapi"]
configure_gen = []
makedepends = ["linux-headers", "musl-bsd-headers"]
pkgdesc = "Transport-independent RPC library"
license = "BSD-3-Clause"
url = "https://libtirpc.sourceforge.net"
source = (
    "https://sourceforge.net/projects/libtirpc/files/libtirpc/1.3.7/"
    "libtirpc-1.3.7.tar.bz2/download>libtirpc-1.3.7.tar.bz2"
)
sha256 = "b47d3ac19d3549e54a05d0019a6c400674da716123858cfdb6d3bdd70a66c702"
# no test suite in the Oasis recipe
options = ["etcfiles", "!check"]


@subpackage("libtirpc-devel")
def _(self):
    return self.default_devel()


def post_install(self):
    self.install_license("COPYING")
