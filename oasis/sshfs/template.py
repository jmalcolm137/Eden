pkgname = "sshfs"
pkgver = "3.6.0"
pkgrel = 0
_commit = "a1e5f12c530ccf59434a7d59a34a049f160b3559"
makedepends = ["fuse-devel"]
depends = ["fuse"]
ignore_shlibs = ["libfuse3.so.3"]
pkgdesc = "FUSE SSH filesystem"
license = "GPL-2.0-or-later"
url = "https://github.com/libfuse/sshfs"
source = f"https://github.com/libfuse/sshfs/archive/{_commit}.tar.gz"
sha256 = "e9be550dc987bd1a386fe05b7e7bfaae7e643f3e62f6114859ecb68ad7d8e41b"
# no test suite in the Oasis recipe
options = ["!check"]


def pre_build(self):
    self.cp(self.files_path / "config.h", self.cwd / "config.h")
    self.cp(self.files_path / "sshfs.1", self.cwd / "sshfs.1")


def build(self):
    from cbuild.util import compiler

    cc = compiler.C(self)
    cc.invoke(
        ["sshfs.c", "nocache.c"],
        "sshfs",
        flags=[
            "-D_FILE_OFFSET_BITS=64", "-D_GNU_SOURCE", "-DFUSE_USE_VERSION=30",
            "-I.", "-I/usr/include/fuse3",
        ],
        ldflags=["-lfuse3", "-lpthread"],
    )


def install(self):
    self.install_bin("sshfs")
    self.install_man("sshfs.1")
    self.install_license("COPYING")
