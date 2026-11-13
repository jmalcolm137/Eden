pkgname = "u-config"
pkgver = "0.34.0"
pkgrel = 1
# Oasis pkg/u-config/src
_commit = "e57b719b709f9112b2570a914e5efef7faf0ff03"
pkgdesc = "Small pkg-config implementation"
license = "Unlicense"
url = "https://github.com/skeeto/u-config"
source = f"{url}/archive/{_commit}.tar.gz"
sha256 = "74b0c56833e1e77924c8d7f559f937a79d74505a733626a2b07239042dcda0f8"
# no test suite in the Oasis recipe
options = ["!check"]

_cflags = [
    "-std=c99",
    "-Wall",
    "-Wpedantic",
    '-DPKG_CONFIG_PREFIX="/usr"',
    '-DPKG_CONFIG_SYSTEM_INCLUDE_PATH=PKG_CONFIG_PREFIX "/include"',
    '-DPKG_CONFIG_SYSTEM_LIBRARY_PATH=PKG_CONFIG_PREFIX "/lib"',
]


def build(self):
    from cbuild.util import compiler

    cc = compiler.C(self)
    cc.invoke(["main_posix.c"], "u-config", flags=_cflags)


def install(self):
    self.install_bin("u-config")
    self.install_man("u-config.1")
    self.install_link("usr/bin/pkg-config", "u-config")
    self.install_link("usr/share/man/man1/pkg-config.1", "u-config.1")
    self.install_license("UNLICENSE")
