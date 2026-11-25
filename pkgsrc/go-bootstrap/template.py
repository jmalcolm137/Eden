pkgname = "go-bootstrap"
pkgver = "1.27.4"
pkgrel = 0
archs = ["x86_64"]
pkgdesc = "Go programming language bootstrap toolchain"
license = "BSD-3-Clause"
url = "https://go.dev"
source = f"https://go.dev/dl/go{pkgver}.linux-amd64.tar.gz"
sha256 = "7226736c2339719cda28fbf3a54d71aa63bcefe376e98cef00034268dab24840"
# prebuilt upstream binaries; stripping or testing them is pointless
options = ["!check", "!strip"]


def install(self):
    # the bootstrap only needs the toolchain, not the docs or test suite;
    # its test data contains binaries with executable stacks
    for d in ["api", "doc", "test"]:
        p = self.cwd / d
        if p.exists():
            self.rm(p, recursive=True)
    for p in list((self.cwd / "src").rglob("testdata")):
        self.rm(p, recursive=True)

    # cbuild already strips the top-level go/ directory
    self.install_files(self.cwd, "usr/lib", name="go-bootstrap")
    self.install_license("LICENSE")
