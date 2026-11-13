pkgname = "linux-personality"
pkgver = "1.0"
pkgrel = 0
pkgdesc = "Minimal linux64/linux32 personality shims for cbuild"
license = "custom:meta"
url = "https://oasislinux.org"
# no tests; only installs the two personality command shims
options = ["!check", "bootstrap"]


def install(self):
    self.install_bin(self.files_path / "linux64")
    self.install_bin(self.files_path / "linux32")
