pkgname = "sbase"
pkgver = "0.1"
pkgrel = 1
build_style = "makefile"
make_build_args = ["MANPREFIX=/usr/share/man"]
make_install_args = ["MANPREFIX=/usr/share/man"]
hostmakedepends = ["byacc"]
pkgdesc = "Suckless core utilities from Oasis"
license = "MIT"
url = "https://github.com/michaelforney/sbase"
source = ("https://github.com/michaelforney/sbase/archive/"
          "6a3d80e430ea3155aaa4123944f7c5bf4995a728.tar.gz")
sha256 = "77ce4f6d66541a548d9b539dadbe1d3d2107af1862472a333c11edc65595e0b8"
# upstream provides a manual tests target, not a make check target
options = ["!check", "bootstrap"]


def post_install(self):
    self.install_license("LICENSE")
    # Many upstream Makefiles invoke plain `install`; sbase calls it xinstall.
    self.install_link("usr/bin/install", "xinstall")
    # Keep the Oasis make at /usr/bin/make. cbuild is patched to use
    # /usr/bin/gmake for GNU make. Drop the sbase tools that conflict with
    # hard requirements: Chimera musl provides getconf, llvm-binutils
    # provides strings/strip/objcopy, bsdtar is needed for compressed
    # sources, and autoconf rejects sbase grep/sed in favour of GNU ones.
    for f in [
        "usr/bin/cmp",
        "usr/bin/egrep",
        "usr/bin/fgrep",
        "usr/bin/getconf",
        "usr/bin/grep",
        "usr/bin/sed",
        "usr/bin/strings",
        "usr/bin/tar",
    ]:
        self.uninstall(f, missing_ok=True)
