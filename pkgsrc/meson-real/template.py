pkgname = "meson-real"
pkgver = "1.9.1"
pkgrel = 1
hostmakedepends = ["python"]
makedepends = ["python-devel"]
depends = ["python", "samurai"]
pkgdesc = "Meson build system"
license = "Apache-2.0"
url = "https://mesonbuild.com"
source = f"https://github.com/mesonbuild/meson/releases/download/{pkgver}/meson-{pkgver}.tar.gz"
sha256 = "4e076606f2afff7881d195574bddcd8d89286f35a17b4977a216f535dc0c74ac"
# Meson's own test suite is huge and not needed for a build tool
options = ["!check"]


def build(self):
    pass


def install(self):
    self.install_files("mesonbuild", "usr/lib/python3.15/site-packages")
    self.install_file("meson.py", "usr/bin", name="meson", mode=0o755)
    # samurai is CLI-compatible with ninja
    ninja = self.cwd / "ninja"
    ninja.write_text("#!/bin/sh\nexec samu \"$@\"\n")
    self.install_file("ninja", "usr/bin", mode=0o755)
    self.install_license("COPYING")
