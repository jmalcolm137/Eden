pkgname = "libliftoff"
pkgver = "0.5.0"
pkgrel = 0
# Oasis pkg/libliftoff/src
_commit = "8b08dc1c14fd019cc90ddabe34ad16596b0691f4"
build_style = "meson"
makedepends = ["libdrm-devel", "linux-headers"]
pkgdesc = "Lightweight KMS plane library"
license = "MIT"
url = "https://gitlab.freedesktop.org/emersion/libliftoff"
source = f"{url}/-/archive/{_commit}/libliftoff-{_commit}.tar.gz"
sha256 = "8de28aee6f90f47b7fc7037dcd2360166197c0b5d2033f3afdbd34f2ea1bf216"
# no test suite in the Oasis recipe
options = ["!check"]


def pre_configure(self):
    p = self.cwd / "meson.build"
    lines = p.read_text().splitlines()
    lines = [
        ln
        for ln in lines
        if "subdir('test')" not in ln and "subdir('example')" not in ln
    ]
    p.write_text("\n".join(lines) + "\n")


@subpackage("libliftoff-devel")
def _(self):
    return self.default_devel()


def post_install(self):
    self.install_license("LICENSE")
