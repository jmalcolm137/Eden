pkgname = "pounce"
pkgver = "3.0"
pkgrel = 0
makedepends = [
    "bearssl-devel-static",
    "libtls-bearssl-devel",
    "libtls-bearssl-devel-static",
]
pkgdesc = "IRC bouncer"
license = "ISC"
url = "https://git.causal.agency/pounce"
source = "https://git.causal.agency/pounce/snapshot/pounce-3.0.tar.gz"
sha256 = "f776f7f170493697a97923e7dce9597dff5577fd40ba756e9a1bcfab17199df0"
# no test suite in the Oasis recipe
options = ["!check"]

_cflags = [
    "-std=c11", "-Wall", "-Wextra", "-Wpedantic", "-D_GNU_SOURCE",
]

_ldflags = ["/usr/lib/libtls.a", "/usr/lib/libbearssl.a", "-lpthread"]


def build(self):
    from cbuild.util import compiler

    cc = compiler.C(self)
    cc.invoke(
        ["bounce.c", "client.c", "config.c", "local.c", "ring.c",
         "server.c", "state.c", "xdg.c"],
        "pounce",
        flags=_cflags,
        ldflags=_ldflags,
    )
    cc.invoke(["dispatch.c"], "calico", flags=_cflags)


def install(self):
    self.install_bin("pounce")
    self.install_bin("calico")
    self.install_man("pounce.1")
    self.install_man("calico.1")
    self.install_license("LICENSE")
