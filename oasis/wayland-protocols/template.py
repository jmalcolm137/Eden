pkgname = "wayland-protocols"
pkgver = "1.31"
pkgrel = 0
# Oasis pkg/wayland-protocols/src
_commit = "4624cfaaf563cd7be5e2e2087c8de6d3a48ea867"
build_style = "meson"
configure_args = ["-Dtests=false"]
pkgdesc = "Wayland protocol extensions"
license = "MIT"
url = "https://gitlab.freedesktop.org/wayland/wayland-protocols"
source = (
    f"{url}/-/archive/{_commit}/wayland-protocols-{_commit}.tar.gz"
)
sha256 = "c9c7364bc59fb9421e3f87c421b87ef910e140b4b8144511106dee4bf5f78f18"
# no test suite in the Oasis recipe
options = ["!check"]


def post_install(self):
    self.install_license("COPYING")
