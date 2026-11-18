pkgname = "libtls-bearssl"
pkgver = "0.6"
pkgrel = 0
build_style = "makefile"
make_build_env = {
    "PREFIX": "/usr",
    "INCDIR": "/usr/include",
    "LIBDIR": "/usr/lib",
    "MANDIR": "/usr/share/man",
    "LDLIBS": "-lbearssl -lpthread",
}
make_install_env = dict(make_build_env)
make_use_env = True
hostmakedepends = ["pkgconf"]
makedepends = ["bearssl-devel"]
pkgdesc = "LibTLS implementation on top of BearSSL for Oasis"
license = "ISC"
url = "https://git.sr.ht/~mcf/libtls-bearssl"
source = f"{url}/archive/{pkgver}.tar.gz"
sha256 = "bd6d6b1cf3f91aa30f1008b739ae787009ffc3d55276c7779a91cffdafa59474"
# tests need brssl/x509cert and network; package build is enough
options = ["!check"]


def post_install(self):
    self.install_license("LICENSE")


@subpackage("libtls-bearssl-devel")
def _(self):
    return [
        "usr/include",
        "usr/lib/libtls.so",
        "usr/lib/pkgconfig",
        "usr/share/man/man3",
    ]


@subpackage("libtls-bearssl-devel-static")
def _(self):
    return ["usr/lib/*.a"]
