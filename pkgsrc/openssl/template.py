pkgname = "openssl"
pkgver = "3.5.9"
pkgrel = 1
archs = ["x86_64"]
hostmakedepends = ["perl"]
makedepends = ["linux-headers", "zlib"]
pkgdesc = "Toolkit for the Transport Layer Security protocol"
license = "Apache-2.0"
url = "https://www.openssl.org"
source = f"https://www.openssl.org/source/openssl-{pkgver}.tar.gz"
sha256 = "603f5602e2eef00d77fbd429d34dcd5822bb301757a1bc9cdb24c670f1eb859a"
# the test suite needs network and a full build environment
options = ["!check", "!lto"]


def configure(self):
    self.do(
        "perl",
        "Configure",
        "shared",
        "zlib",
        "no-tests",
        "--prefix=/usr",
        "--openssldir=/etc/ssl",
        "--libdir=lib",
        "--release",
    )


def build(self):
    self.do("gmake", f"-j{self.make_jobs}")


def install(self):
    self.do(
        "gmake",
        f"DESTDIR={self.chroot_destdir}",
        "install_sw",
    )
    self.install_license("LICENSE.txt")


@subpackage("openssl-progs")
def _(self):
    self.pkgdesc = "OpenSSL command line tool"
    # keep the CLI out of the library package so it can coexist with
    # libressl (both provide /usr/bin/openssl)
    return ["usr/bin"]
