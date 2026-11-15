pkgname = "xz"
pkgver = "5.8.4"
pkgrel = 1
build_style = "gnu_configure"
configure_args = ["--disable-nls", "--disable-sandbox"]
configure_gen = []
hostmakedepends = ["pkgconf"]
makedepends = []
renames = ["liblzma"]
pkgdesc = "XZ compression utilities"
license = "0BSD"
url = "https://tukaani.org/xz"
source = f"https://github.com/tukaani-project/xz/releases/download/v{pkgver}/xz-{pkgver}.tar.gz"
sha256 = "0014c7886930454fe8bd4228665b51af55eeae560ea135c9c4cd33f55b2591d9"
options = ["bootstrap"]


if self.stage > 0:
    makedepends += ["linux-headers"]


def pre_configure(self):
    # We use the pre-generated autotools files; keep make from trying to
    # regenerate them after the patches touch configure.ac/Makefile.am.
    for f in list(self.cwd.rglob("Makefile.in")):
        f.touch()
    for f in ("aclocal.m4", "configure", "config.h.in"):
        p = self.cwd / f
        if p.exists():
            p.touch()


def post_install(self):
    self.install_license("COPYING")
    self.uninstall("usr/share/doc")
    for tool in [
        "xzgrep",
        "xzfgrep",
        "xzegrep",
        "lzgrep",
        "lzfgrep",
        "lzegrep",
        "xzdiff",
        "lzdiff",
        "xzcmp",
        "lzcmp",
        "xzless",
        "xzmore",
        "lzless",
        "lzmore",
    ]:
        self.uninstall(f"usr/bin/{tool}")
        self.uninstall(f"usr/share/man/man1/{tool + '.1'}")


@subpackage("xz-devel")
def _(self):
    self.renames = ["liblzma-devel"]

    return self.default_devel()
