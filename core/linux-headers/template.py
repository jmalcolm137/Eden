pkgname = "linux-headers"
pkgver = "7.3.5"
pkgrel = 0
# x86_64 only for the initial source-bootstrap toolchain; other
# architectures can be restored once this path is working.
archs = ["x86_64"]
hostmakedepends = ["gmake", "perl"]
pkgdesc = "Linux API headers for userland development"
license = "GPL-2.0-only"
url = "https://www.kernel.org"
source = f"https://github.com/CachyOS/linux/releases/download/cachyos-{pkgver}-2/cachyos-{pkgver}-2.tar.gz"
sha256 = "bb22ad99e1042fae883bab71366f8339367b74c045004fe92ad4923339092e07"
# nothing to test
options = ["bootstrap", "!check"]

# x86_64 only for the bootstrap toolchain (other arches deferred)
_arch = "x86_64"

def build(self):
    self.do(
        "gmake",
        "ARCH=" + _arch,
        "CC=clang",
        "HOSTCC=clang",
        "mrproper",
        "headers",
    )

    # remove extra files and drm headers
    for fn in self.find(".", ".*", files=True):
        self.rm(fn)

    self.rm("usr/include/Makefile")
    self.rm("usr/include/drm", recursive=True)


def install(self):
    self.install_files("usr/include", "usr")
