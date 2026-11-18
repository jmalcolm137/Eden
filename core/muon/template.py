pkgname = "muon"
pkgver = "0.7.1"
pkgrel = 1
makedepends = [
    "libatomic-chimera-devel-static",
    "libunwind-devel-static",
    "musl-devel-static",
]
pkgdesc = "Meson-compatible build system from Oasis"
license = "GPL-3.0-only AND Apache-2.0 AND MIT AND Unlicense"
url = "https://muon.build"
source = f"https://git.sr.ht/~lattis/muon/archive/{pkgver}.tar.gz"
sha256 = "967a99ade648a850807d5637c80d55043ded34556e9dcbfec8736d6de52f96c5"
# no tests during bootstrap package builds
options = ["!check", "bootstrap"]


def build(self):
    self.do(self.chroot_cwd / "bootstrap.sh", "build")
    self.do(
        self.chroot_cwd / "build/muon-bootstrap",
        "setup", "-Dprefix=/usr",
        "-Dc_link_args=-static-pie", "-Dcpp_link_args=-static-pie",
        "build-out",
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
