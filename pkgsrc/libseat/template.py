pkgname = "libseat"
pkgver = "0.9.3"
pkgrel = 1
build_style = "meson"
configure_args = [
    "-Dexamples=disabled",
    "-Dlibseat-builtin=enabled",
    "-Dlibseat-logind=disabled",
    "-Dlibseat-seatd=enabled",
    "-Dman-pages=disabled",
]
hostmakedepends = ["muon", "pkgconf", "samurai"]
makedepends = ["linux-headers"]
pkgdesc = "Universal seat management library"
license = "MIT"
url = "https://sr.ht/~kennylevinsen/seatd"
source = f"https://git.sr.ht/~kennylevinsen/seatd/archive/{pkgver}.tar.gz"
sha256 = "302564d54d8e28191fadfd734f2675ecb0c9e0615a58011b89ef15dfa4dbaa96"
# tests need a live seat and root privileges
options = ["!check"]


@subpackage("libseat-devel")
def _(self):
    return self.default_devel()


@subpackage("libseat-progs")
def _(self):
    self.provides = [self.with_pkgver("seatd")]
    return self.default_progs()


def post_install(self):
    self.install_license("LICENSE")
