pkgname = "libevdev"
pkgver = "1.12.0"
pkgrel = 0
# Oasis pkg/libevdev/src
_commit = "69403a63ed29a1ee62edb8d0885fa770dd9a53cf"
build_style = "meson"
configure_args = ["-Dtests=disabled", "-Ddocumentation=disabled"]
hostmakedepends = ["python"]
makedepends = ["linux-headers"]
pkgdesc = "Wrapper library for evdev devices"
license = "MIT"
url = "https://gitlab.freedesktop.org/libevdev/libevdev"
source = f"{url}/-/archive/{_commit}/libevdev-{_commit}.tar.gz"
sha256 = "c920f89f3c71807f625decae655f58be1d93a29cfdc729887b6ebb67a76c0f17"
# no test suite in the Oasis recipe
options = ["!check"]


def pre_configure(self):
    p = self.cwd / "meson_options.txt"
    p.write_text(p.read_text().replace("value: 'false'", "value: false"))


@subpackage("libevdev-devel")
def _(self):
    return self.default_devel()


def post_install(self):
    self.install_license("COPYING")
