pkgname = "libressl"
pkgver = "4.3.1"
pkgrel = 2
build_style = "gnu_configure"
configure_args = ["--disable-tests"]
configure_gen = []
hostmakedepends = ["perl", "pkgconf"]
makedepends = [
    "libatomic-chimera-devel-static",
    "musl-devel-static",
    "zlib-static",
]
pkgdesc = "OpenBSD TLS and cryptography library"
license = "OpenSSL"
url = "https://www.libressl.org"
source = f"https://cdn.openbsd.org/pub/OpenBSD/LibreSSL/libressl-{pkgver}.tar.gz"
sha256 = "c2db42ace14e7d5419826fab35a742ec6e4d12725a051a51d0cea3c10ba0fa50"
# no test suite in the Oasis recipe
options = ["etcfiles", "!check"]


@subpackage("libressl-devel")
def _(self):
    return self.default_devel()


def post_build(self):
    # Keep the shared libraries for consumers and relink the two tools
    # against the static archives.
    from cbuild.util import compiler

    cc = compiler.C(self)
    libs = [
        "build/tls/.libs/libtls.a",
        "build/ssl/.libs/libssl.a",
        "build/crypto/.libs/libcrypto.a",
        "-lpthread",
        "-lm",
        "-lz",
        "-static-pie",
        "-unwindlib=none",
    ]
    objs = [
        str(p.relative_to(self.cwd))
        for p in sorted((self.cwd / "build/apps/openssl").glob("*.o"))
    ]
    cc.invoke(objs, "openssl-static", ldflags=libs)
    cc.invoke(
        [
            "build/apps/ocspcheck/ocspcheck.o",
            "build/apps/ocspcheck/http.o",
        ],
        "ocspcheck-static",
        ldflags=libs,
    )


def post_install(self):
    self.install_license("COPYING")
    for name in ["openssl", "ocspcheck"]:
        self.uninstall(f"usr/bin/{name}", missing_ok=True)
        self.install_bin(f"{name}-static", name=name)
