pkgname = "rc"
pkgver = "0_git20200101"
pkgrel = 0
# Oasis pkg/rc/src
_commit = "1884d8fe62c22b3bb0676f570c25473faa340c3c"
makedepends = ["byacc"]
pkgdesc = "Plan 9 command interpreter"
license = "custom:rc"
url = "https://github.com/oasislinux/rc"
source = f"{url}/archive/{_commit}.tar.gz"
sha256 = "f9edb4ebb2839e32d6993853a1c73b24fd49af8553ea17162b57be38d6a9a0f7"
# no test suite in the Oasis recipe
options = ["!distlicense", "!check"]

_cflags = ["-Wpedantic", "-I.", '-DPREFIX="/usr"']


def pre_build(self):
    self.do("byacc", "-d", "syn.y")


def build(self):
    from cbuild.util import compiler

    cc = compiler.C(self)
    cc.invoke(
        [
            "code.c",
            "exec.c",
            "getflags.c",
            "glob.c",
            "here.c",
            "io.c",
            "lex.c",
            "pcmd.c",
            "pfnc.c",
            "simple.c",
            "subr.c",
            "trap.c",
            "tree.c",
            "var.c",
            "havefork.c",
            "unix.c",
            "y.tab.c",
        ],
        "rc",
        flags=_cflags,
    )


def install(self):
    self.install_bin("rc")
    self.install_man("rc.1")
    self.install_file("rcmain.unix", "usr/lib", mode=0o644, name="rcmain")
