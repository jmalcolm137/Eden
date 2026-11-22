pkgname = "fuse3"
pkgver = "3.18.3"
pkgrel = 0
archs = ["x86_64"]
build_style = "meson"
configure_args = [
    "-Dexamples=false",
    "-Dinitscriptdir=",
    "-Dtests=false",
    "-Dudevrulesdir=",
    "-Duseroot=false",
    "-Dutils=true",
    "-Ddisable-libc-symbol-version=true",
    "-Dc_link_args=-Wl,--undefined-version",
]
hostmakedepends = ["meson-real", "pkgconf", "samurai"]
makedepends = ["linux-headers"]
pkgdesc = "Reference implementation of the Linux FUSE interface"
license = "GPL-2.0-only AND LGPL-2.1-only"
url = "https://github.com/libfuse/libfuse"
source = f"https://github.com/libfuse/libfuse/releases/download/fuse-{pkgver}/fuse-{pkgver}.tar.gz"
sha256 = "bcd19582c5e30f7fe45dd86a5540e998590aa01903afc7ebcbeea6c8ac5421ee"
file_modes = {"usr/bin/fusermount3": ("root", "root", 0o4755)}
# the test suite needs a working FUSE mount
options = ["!check", "etcfiles"]


@subpackage("fuse3-devel")
def _(self):
    return self.default_devel()


def post_install(self):
    self.install_license("LICENSE")
