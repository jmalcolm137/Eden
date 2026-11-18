pkgname = "libdrm"
pkgver = "2.4.134"
pkgrel = 0
build_style = "meson"
configure_args = [
    "-Dintel=disabled",
    "-Dudev=true",
    "-Dvalgrind=disabled",
]
hostmakedepends = [
    "muon",
    "pkgconf",
    "python",
    "samurai",
]
makedepends = ["linux-headers", "udev-devel"]
pkgdesc = "Userspace interface to kernel DRM services"
license = "MIT"
url = "https://dri.freedesktop.org"
source = "https://gitlab.freedesktop.org/mesa/drm/-/archive/libdrm-2.4.134/drm-libdrm-2.4.134.tar.gz"
sha256 = "6b18e4834b0c061232cb5c11e98a6ecdc72ebc6bc282d124406b7a9d4e089ce2"
# the test suite needs a DRM device
options = ["!check", "!distlicense"]


@subpackage("libdrm-devel")
def _(self):
    return self.default_devel()