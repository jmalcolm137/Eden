pkgname = "libglvnd"
pkgver = "1.7.0"
pkgrel = 1
build_style = "meson"
configure_args = [
    "-Degl=true",
    "-Dgles1=true",
    "-Dgles2=true",
    "-Dglx=disabled",
    "-Dtls=true",
    "-Dx11=disabled",
]
hostmakedepends = [
    "muon",
    "pkgconf",
    "python",
    "samurai",
]
pkgdesc = "GL vendor-neutral dispatch library"
license = "custom:glvnd"
url = "https://gitlab.freedesktop.org/glvnd/libglvnd"
source = "https://gitlab.freedesktop.org/glvnd/libglvnd/-/archive/v1.7.0/libglvnd-v1.7.0.tar.gz"
sha256 = "2b6e15b06aafb4c0b6e2348124808cbd9b291c647299eaaba2e3202f51ff2f3d"
# tests require a display or a full graphics stack
options = ["!check"]


def post_install(self):
    self.install_license("README.md")


@subpackage("libglvnd-devel")
def _(self):
    return self.default_devel()
