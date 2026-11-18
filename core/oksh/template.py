pkgname = "oksh"
pkgver = "7.9"
pkgrel = 2
build_style = "configure"
configure_args = [
    "--prefix=/usr",
    "--enable-ksh",
    "--enable-sh",
    "--enable-small",
]
makedepends = [
    "libatomic-chimera-devel-static",
    "libunwind-devel-static",
    "musl-devel-static",
]
pkgdesc = "Portable Korn shell from Oasis"
license = "BSD-3-Clause"
url = "https://github.com/ibara/oksh"
source = f"https://github.com/ibara/oksh/archive/refs/tags/oksh-{pkgver}.tar.gz"
sha256 = "1dc923da1a2bd52d4035e2ae0463d8fed353339d6e692ff747926d2125346f2e"
tool_flags = {"LDFLAGS": ["-static-pie"]}
# upstream has no check target
options = ["!check", "bootstrap"]


def post_install(self):
    self.install_license("LEGAL")
