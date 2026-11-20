pkgname = "libuuid"
pkgver = "2.41.3"
pkgrel = 1
build_style = "gnu_configure"
configure_args = [
    "--disable-all-programs",
    "--disable-nls",
    "--disable-static",
    "--enable-libuuid",
    "--without-ncurses",
    "--without-ncursesw",
    "--without-systemd",
    "--without-udev",
]
configure_gen = []
hostmakedepends = ["pkgconf"]
pkgdesc = "Universally unique identifier library from util-linux"
license = "BSD-3-Clause"
url = "https://www.kernel.org/pub/linux/utils/util-linux"
source = f"https://www.kernel.org/pub/linux/utils/util-linux/v2.41/util-linux-{pkgver}.tar.gz"
sha256 = "24160e7c3bfc6feecb9076706437fdb1212817549aaf9b4408f5a8e0b94e3eca"
# no test suite for the standalone library build
options = ["!check"]


@subpackage("libuuid-devel")
def _(self):
    return self.default_devel()


def post_install(self):
    self.install_license("Documentation/licenses/COPYING.BSD-3-Clause")
