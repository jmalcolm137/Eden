pkgname = "x509cert"
pkgver = "0.4"
pkgrel = 0
# Oasis pkg/x509cert/src
_commit = "f25cb85dc71dce619c3fbb9e4aa28e3e9beba1ff"
makedepends = ["bearssl-devel", "bearssl-devel-static"]
pkgdesc = "X.509 certificate utility"
license = "ISC"
url = "https://git.sr.ht/~mcf/x509cert"
source = f"{url}/archive/{_commit}.tar.gz"
sha256 = "c82260e52aa7ea9e7e2d9997ca26104a8e1aecf99620afdf717183873b0319f1"
# no test suite in the Oasis recipe
options = ["!check"]

_cflags = ["-std=c99", "-Wall", "-Wpedantic", "-I."]

_lib_sources = [
    "cert.c",
    "der.c",
    "dn.c",
    "dn_string.c",
    "oid.c",
    "pkey.c",
    "req.c",
    "san.c",
    "sign.c",
]


def build(self):
    from cbuild.util import compiler

    cc = compiler.C(self)
    self.mkdir("obj", parents=True)
    objs = []
    for src in _lib_sources:
        obj = "obj/" + src.removesuffix(".c") + ".o"
        cc.invoke([src], obj, obj_file=True, flags=_cflags)
        objs.append(obj)
    self.do("ar", "rcs", "libx509cert.a", *objs)
    cc.invoke(
        ["x509cert.c", "libx509cert.a"],
        "x509cert",
        flags=_cflags,
        ldflags=["/usr/lib/libbearssl.a"],
    )


def install(self):
    self.install_bin("x509cert")
    self.install_man("x509cert.1")
    self.install_lib("libx509cert.a", mode=0o644)
    self.install_file("x509cert.h", "usr/include")
    self.install_license("LICENSE")


@subpackage("x509cert-devel")
def _(self):
    return ["usr/include"]


@subpackage("x509cert-devel-static")
def _(self):
    return ["usr/lib/*.a"]
