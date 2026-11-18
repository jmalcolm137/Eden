pkgname = "ubase"
pkgver = "0.1"
pkgrel = 1
build_style = "makefile"
make_build_args = ["MANPREFIX=/usr/share/man", "LDFLAGS=-static-pie"]
make_install_args = ["MANPREFIX=/usr/share/man"]
makedepends = ["libatomic-chimera-devel-static", "libunwind-devel-static", "musl-devel-static"]
pkgdesc = "Suckless base utilities from Oasis"
license = "MIT"
url = "https://github.com/michaelforney/ubase"
source = ("https://github.com/michaelforney/ubase/archive/"
          "f152e7fc3bd1675060818ac224f96541a2d9d6e7.tar.gz")
sha256 = "be319d03ee878a27969495043b15d955afb78efa3286531ee86d0d747a6522c4"
# upstream has no check target
options = ["!check", "bootstrap"]


def post_patch(self):
    # cbuild's makefile style passes its own LDFLAGS on the command line;
    # force the static-pie link for the Oasis base utilities
    p = self.cwd / "Makefile"
    text = p.read_text()
    text = text.replace(
        "include config.mk", "include config.mk\n\noverride LDFLAGS += -static-pie", 1
    )
    p.write_text(text)


def post_install(self):
    self.install_license("LICENSE")
