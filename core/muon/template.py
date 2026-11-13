pkgname = "muon"
pkgver = "0.7.0"
pkgrel = 0
pkgdesc = "Meson-compatible build system from Oasis"
license = "GPL-3.0-only AND Apache-2.0 AND MIT AND Unlicense"
url = "https://muon.build"
source = f"https://git.sr.ht/~lattis/muon/archive/{pkgver}.tar.gz"
sha256 = "e7095741dc11338f5ed8e0aa02e993fc34df4295dad4296127bbb212bcf56e07"
# no tests during bootstrap package builds
options = ["!check", "bootstrap"]


def build(self):
    self.do(self.chroot_cwd / "bootstrap.sh", "build")
    self.do(
        self.chroot_cwd / "build/muon-bootstrap",
        "setup", "-Dprefix=/usr", "build-out",
        env={"CC": "clang", "CXX": "clang++"},
    )
    self.do(
        self.chroot_cwd / "build/muon-bootstrap",
        "-C", "build-out", "samu",
        env={"CC": "clang", "CXX": "clang++"},
    )


def install(self):
    self.do(
        self.chroot_cwd / "build-out/muon",
        "-C", "build-out", "install",
        env={"DESTDIR": str(self.chroot_destdir)},
    )
    self.install_license("LICENSES/MIT.txt")
