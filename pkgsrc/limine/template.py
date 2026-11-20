pkgname = "limine"
pkgver = "12.9.0"
pkgrel = 0
archs = ["x86_64"]
hostmakedepends = ["automake", "nasm"]
pkgdesc = "Multiprotocol EFI bootloader"
license = "BSD-2-Clause AND 0BSD"
url = "https://limine-bootloader.org"
source = f"https://github.com/Limine-Bootloader/Limine/releases/download/v{pkgver}/limine-{pkgver}.tar.gz"
sha256 = "adea922af3b9c8179a4676bcecc8e4df2f3ef72ad36b3f4afab44cbf5f265e36"
# no test suite
options = ["!check"]


def build(self):
    self.do("./configure", "--prefix=/usr", "--enable-bios", "--enable-uefi-x86_64")
    self.do("gmake", f"-j{self.make_jobs}")


def install(self):
    self.do(
        "gmake",
        "install",
        f"DESTDIR={self.chroot_destdir}",
        "PREFIX=/usr",
    )


def post_install(self):
    self.uninstall("usr/share/doc/limine/COPYING", missing_ok=True)
    self.install_license("COPYING")
