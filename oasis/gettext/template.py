pkgname = "gettext"
pkgver = "1.0"
pkgrel = 1
build_style = "gnu_configure"
configure_args = [
    "--disable-csharp",
    "--disable-java",
    "--disable-libasprintf",
    "--disable-openmp",
    "--without-emacs",
    "--without-git",
    "--with-xz",
]
configure_gen = []
hostmakedepends = ["xz"]
makedepends = ["linux-headers"]
pkgdesc = "GNU internationalization utilities"
license = "GPL-3.0-or-later"
url = "https://www.gnu.org/software/gettext"
source = "https://ftp.gnu.org/gnu/gettext/gettext-1.0.tar.gz"
sha256 = "85d99b79c981a404874c02e0342176cf75c7698e2b51fe41031cf6526d974f1a"
# most tests need a specific shell and locale setup
options = ["!check"]


def post_install(self):
    self.install_license("COPYING")


@subpackage("gettext-devel")
def _(self):
    return self.default_devel()
