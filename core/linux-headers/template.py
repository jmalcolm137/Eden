pkgname = "linux-headers"
pkgver = "7.0.12"
pkgrel = 0
# x86_64 only for the initial source-bootstrap toolchain; other
# architectures can be restored once this path is working.
archs = ["x86_64"]
hostmakedepends = ["gmake", "perl"]
pkgdesc = "Linux API headers for userland development"
license = "GPL-2.0-only"
url = "https://www.kernel.org"
source = f"$(KERNEL_SITE)/kernel/v{pkgver[0]}.x/linux-{pkgver}.tar.xz"
sha256 = "57edc9a41efc1ca6b797afa8f4a587a30da2af6bca7356eb56e1e1a4ada265da"
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
