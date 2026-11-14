pkgname = "efibootmgr"
pkgver = "18"
pkgrel = 0
# Oasis pkg/efibootmgr/src
_commit = "c3f9f0534e32158f62c43564036878b93b9e0fd6"
makedepends = ["efivar", "efivar-devel", "linux-headers"]
pkgdesc = "EFI boot manager"
license = "GPL-2.0-or-later"
url = "https://github.com/rhinstaller/efibootmgr"
source = f"{url}/archive/{_commit}.tar.gz"
sha256 = "e922259fbd223ca8d028a7bb4f9e01aa6c8b560c7c5281d7e96b62557936cc33"
# no test suite in the Oasis recipe
options = ["!check"]

_cflags = [
    "-std=c99",
    "-Wall",
    '-DEFIBOOTMGR_VERSION="18"',
    '-DDEFAULT_LOADER="/linux"',
    "-I.",
    "-Isrc/include",
    "-I/usr/include/efivar",
]


def pre_build(self):
    text = (self.cwd / "src/efibootmgr.8.in").read_text()
    (self.cwd / "efibootmgr.8").write_text(text.replace("@@DEFAULT_LOADER@@", "/linux"))


def build(self):
    from cbuild.util import compiler

    cc = compiler.C(self)
    cc.invoke(
        ["src/efibootmgr.c", "src/efi.c", "src/parse_loader_data.c"],
        "efibootmgr",
        flags=_cflags,
        ldflags=["/usr/lib/libefiboot.a", "/usr/lib/libefivar.a"],
    )


def install(self):
    self.install_bin("efibootmgr")
    self.install_man("efibootmgr.8")
    self.install_license("COPYING")
