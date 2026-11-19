pkgname = "sbase"
pkgver = "0.1"
pkgrel = 5
build_style = "makefile"
make_build_args = ["MANPREFIX=/usr/share/man", "LDFLAGS=-static-pie"]
make_install_args = ["MANPREFIX=/usr/share/man"]
hostmakedepends = ["byacc"]
makedepends = ["libatomic-chimera-devel-static", "libunwind-devel-static", "musl-devel-static"]
pkgdesc = "Suckless core utilities from Oasis"
license = "MIT"
url = "https://github.com/michaelforney/sbase"
source = ("https://github.com/michaelforney/sbase/archive/"
          "6a3d80e430ea3155aaa4123944f7c5bf4995a728.tar.gz")
sha256 = "77ce4f6d66541a548d9b539dadbe1d3d2107af1862472a333c11edc65595e0b8"
# upstream provides a manual tests target, not a make check target
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
    # Many upstream Makefiles invoke plain `install`; sbase calls it xinstall.
    self.install_link("usr/bin/install", "xinstall")
    # Keep the Oasis make at /usr/bin/make. cbuild is patched to use
    # /usr/bin/gmake for GNU make. Drop the sbase tools that conflict with
    # hard requirements: Chimera musl provides getconf, llvm-binutils
    # provides strings/strip/objcopy, and bsdtar is needed for compressed
    # sources. sed stays: GNU sed is packaged as gsed and autoconf prefers it.
    for f in [
        "usr/bin/bc",
        "usr/bin/getconf",
        "usr/bin/strings",
        "usr/bin/tar",
    ]:
        self.uninstall(f, missing_ok=True)
