pkgname = "cosmic-sound-theme"
pkgver = "1.11.0"
pkgrel = 0
archs = ["x86_64"]
build_style = "meson"
hostmakedepends = ["meson-real"]
pkgdesc = "Sound theme for the COSMIC desktop environment"
license = "CC-BY-SA-4.0"
url = "https://github.com/pop-os/cosmic-sound-theme"
source = f"https://github.com/pop-os/cosmic-sound-theme/archive/refs/tags/epoch-{pkgver}.tar.gz"
sha256 = "b523afe23c4b5bb58261156564b7527a1f719bc9b9917f9c6bd3c763d823291c"
# upstream has no test suite
options = ["!check"]


def post_install(self):
    self.install_license("LICENSE")
