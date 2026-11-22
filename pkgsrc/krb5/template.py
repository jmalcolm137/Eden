pkgname = "krb5"
pkgver = "1.22.3"
pkgrel = 0
archs = ["x86_64"]
build_style = "gnu_configure"
configure_script = "src/configure"
configure_args = [
    "--disable-static",
    "--enable-dns-for-realm",
    "--without-ldap",
    "--without-system-verto",
]
# the release tarball ships the generated configure script
configure_gen = []
hostmakedepends = ["gmake", "perl", "pkgconf"]
makedepends = ["openssl", "zlib"]
pkgdesc = "MIT Kerberos network authentication protocol"
license = "MIT"
url = "https://web.mit.edu/kerberos"
source = f"https://kerberos.org/dist/krb5/1.22/krb5-{pkgver}.tar.gz"
sha256 = "fe90af8441ad9fa9b064b8e53077cefb782a96f8a68276b031dc54af1789ff0b"
# upstream test suite needs network and a functioning KDC
options = ["!check", "!lto"]


def install(self):
    self.do(
        "gmake",
        "-C",
        "build",
        "install",
        f"DESTDIR={self.chroot_destdir}",
    )
    self.install_license("doc/mitK5license.rst")


def post_install(self):
    # ksu is setuid; the library and client tools do not need it
    self.uninstall("usr/bin/ksu")
    self.uninstall("usr/share/man/man1/ksu.1")


@subpackage("krb5-devel")
def _(self):
    return self.default_devel()
