pkgname = "bison"
pkgver = "3.8.2"
pkgrel = 0
build_style = "gnu_configure"
configure_args = ["--disable-nls", "--disable-rpath"]
configure_gen = []
hostmakedepends = ["pkgconf"]
pkgdesc = "GNU parser generator"
license = "GPL-3.0-or-later"
url = "https://www.gnu.org/software/bison"
source = "https://ftp.gnu.org/gnu/bison/bison-3.8.2.tar.xz"
sha256 = "9bba0214ccf7f1079c5d59210045227bcf619519840ebfa80cd3849cff5a5bf2"
# tests need the full upstream test harness
options = ["!check", "!lintstatic"]


def post_install(self):
    self.install_license("COPYING")
    # byacc already provides yacc; keep bison from conflicting with it
    self.uninstall("usr/bin/yacc", missing_ok=True)
