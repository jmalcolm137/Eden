pkgname = "ubase"
pkgver = "0.1"
pkgrel = 0
build_style = "makefile"
make_build_args = ["MANPREFIX=/usr/share/man"]
make_install_args = ["MANPREFIX=/usr/share/man"]
pkgdesc = "Suckless base utilities from Oasis"
license = "MIT"
url = "https://github.com/michaelforney/ubase"
source = ("https://github.com/michaelforney/ubase/archive/"
          "f152e7fc3bd1675060818ac224f96541a2d9d6e7.tar.gz")
sha256 = "be319d03ee878a27969495043b15d955afb78efa3286531ee86d0d747a6522c4"
# upstream has no check target
options = ["!check", "bootstrap"]


def post_install(self):
    self.install_license("LICENSE")
