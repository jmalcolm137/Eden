pkgname = "sbase"
pkgver = "0.1"
pkgrel = 0
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
    # Keep the Oasis make at /usr/bin/make. cbuild is patched to use
    # /usr/bin/gmake for GNU make. Drop the sbase tools that conflict with
    # hard requirements: Chimera musl provides getconf, llvm-binutils
    # provides strings/strip/objcopy, and bsdtar is needed to extract
    # compressed sources (sbase tar does not auto-decompress).
    for f in [
        "usr/bin/getconf",
        "usr/bin/strings",
        "usr/bin/tar",
    ]:
        self.uninstall(f)
