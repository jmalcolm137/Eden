pkgname = "crun"
pkgver = "1.31"
pkgrel = 0
build_style = "gnu_configure"
configure_args = ["--disable-criu", "--disable-static", "--disable-systemd"]
configure_gen = []
hostmakedepends = ["go-md2man", "pkgconf", "python"]
makedepends = [
    "argp-standalone",
    "json-c-devel",
    "libcap-devel",
    "libseccomp-devel",
    "linux-headers",
]
pkgdesc = "Lightweight OCI runtime and container library"
license = "GPL-2.0-or-later AND LGPL-2.1-or-later"
url = "https://github.com/containers/crun"
source = f"{url}/releases/download/{pkgver}/crun-{pkgver}.tar.zst"
sha256 = "cb76a7951438205466725307e4061da6d1dfdc202bdf675cf209c7037b94002b"
# the test suite needs a privileged container environment
options = ["!check"]


@subpackage("crun-devel")
def _(self):
    return self.default_devel()
