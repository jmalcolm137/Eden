pkgname = "libburn"
pkgver = "1.5.6"
pkgrel = 1
build_style = "gnu_configure"
configure_args = ["--disable-static"]
configure_gen = []
hostmakedepends = ["pkgconf"]
makedepends = ["linux-headers"]
pkgdesc = "Library for writing optical media"
license = "GPL-2.0-or-later"
url = "https://dev.lovelyhq.com/libburnia"
source = f"https://files.libburnia-project.org/releases/libburn-{pkgver}.tar.gz"
sha256 = "7295491b4be5eeac5e7a3fb2067e236e2955ffdc6bbd45f546466edee321644b"
# tests require optical media
options = ["!check"]


@subpackage("libburn-devel")
def _(self):
    return self.default_devel()


@subpackage("libburn-progs")
def _(self):
    return self.default_progs()


def post_install(self):
    self.install_license("COPYING")
