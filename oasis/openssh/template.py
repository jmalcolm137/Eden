pkgname = "openssh"
pkgver = "10.6_p2"
pkgrel = 0
build_style = "gnu_configure"
configure_args = [
    "--with-ssl-dir=/usr",
    "--without-openssl-header-check",
    "--with-privsep-path=/var/empty",
    "--with-pid-dir=/run",
    "--with-maildir=/var/mail",
]
configure_gen = []
makedepends = ["libressl-devel", "zlib-ng-compat-devel"]
pkgdesc = "OpenBSD Secure Shell"
license = "ISC"
url = "https://www.openssh.com"
source = (
    "https://cdn.openbsd.org/pub/OpenBSD/OpenSSH/portable/"
    f"openssh-{pkgver.replace('_', '')}.tar.gz"
)
sha256 = "9ae44872090cf2f06b3cf9ff147e7f16f309671340763ed2f99248398ae29d5b"
# no test suite in the Oasis recipe
options = ["etcfiles", "!check"]


def post_install(self):
    self.install_license("LICENCE")
    for name in ("ssh-keysign",):
        p = self.destdir / "usr/lib" / name
        if p.exists():
            p.chmod(0o755)
