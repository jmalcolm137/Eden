pkgname = "sinit"
pkgver = "1.0"
pkgrel = 0
# Oasis pkg/sinit/src
_commit = "731f65fc82afcd474f4c682f9f0069e5c80c86dd"
pkgdesc = "Minimal init from Oasis"
license = "MIT"
url = "https://git.suckless.org/sinit"
# suckless does not provide archive snapshots; use a mirror of the same commit
source = f"https://github.com/kesor/suckless-sinit/archive/{_commit}.tar.gz"
sha256 = "7ab559af7d562315c126f088cb45b4884d3aa6ea775508831faf5865dd8cc3f5"
# upstream has no test suite
options = ["!check"]

_cflags = [
    "-std=c99",
    "-Wall",
    "-Wpedantic",
    "-D_POSIX_C_SOURCE=200809L",
    '-DPREFIX=""',
    "-I.",
]


def pre_build(self):
    self.cp(self.files_path / "config.h", "config.h")
    self.cp(self.files_path / "shutdown.c", "shutdown.c")


def build(self):
    from cbuild.util import compiler

    cc = compiler.C(self)
    cc.invoke(["sinit.c"], "sinit", flags=_cflags)
    cc.invoke(["shutdown.c"], "shutdown", flags=_cflags)


def install(self):
    self.install_bin("sinit")
    self.install_link("usr/bin/init", "sinit")
    self.install_file("shutdown", "usr/lib/sinit", mode=0o755)
    self.install_man("sinit.8")
    self.install_license("LICENSE")
