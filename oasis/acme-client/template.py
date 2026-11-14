pkgname = "acme-client"
pkgver = "0_git20260101"
pkgrel = 0
makedepends = [
    "bearssl-devel-static", "byacc", "libtls-bearssl-devel-static",
    "openbsd-devel", "openbsd-devel-static", "x509cert-devel-static",
]
pkgdesc = "ACME client from OpenBSD"
license = "ISC"
url = "https://man.openbsd.org/acme-client"
source = "https://cloudflare.cdn.openbsd.org/pub/OpenBSD/8.0/src.tar.gz"
sha256 = "9984c74ff875b5ff041e4676a7f3e4e1ead2cc47a284d705eb9f37cbec4fe795"
# builds the acme-client subdirectory of the OpenBSD source tree
options = ["!check"]

_srcdir = "usr.sbin/acme-client"

_cflags = [
    "-std=c11", "-Wall", "-Wpedantic", "-Wno-pointer-sign",
    "-D_GNU_SOURCE", "-Iout", f"-I{_srcdir}",
    "-isystem", "/usr/include/openbsd",
]

_sources = [
    "acctproc.c", "base64.c", "certproc.c", "chngproc.c", "dbg.c",
    "dnsproc.c", "fileproc.c", "http.c", "jsmn.c", "json.c",
    "keyproc.c", "main.c", "netproc.c", "revokeproc.c", "key.c",
    "util.c",
]


def build(self):
    from cbuild.util import compiler

    self.mkdir("out", parents=True)
    self.do(
        "byacc", "-d", "-o", "out/parse.tab.c", f"{_srcdir}/parse.y",
    )
    cc = compiler.C(self)
    cc.invoke(
        [f"{_srcdir}/{s}" for s in _sources] + ["out/parse.tab.c"]
        + ["/usr/lib/libtls.a", "/usr/lib/libbearssl.a", "/usr/lib/libx509cert.a", "/usr/lib/libbsd.a"],
        "acme-client",
        flags=_cflags,
    )


def install(self):
    self.install_bin("acme-client")
    self.install_man(f"{_srcdir}/acme-client.1")
    self.install_man(f"{_srcdir}/acme-client.conf.5")
    self.install_license(self.template_path / "LICENSE")
