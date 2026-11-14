pkgname = "ii"
pkgver = "1.9"
pkgrel = 0
pkgdesc = "Minimalist IRC client"
license = "ISC"
url = "https://tools.suckless.org/ii"
# source is the Oasis-pinned suckless commit, vendored under files/
options = ["!check"]

_cflags = ["-Wall", "-Wno-format-truncation", '-DVERSION="1.9"']


def pre_build(self):
    self.cp(self.files_path / "ii.c", "ii.c")
    self.cp(self.files_path / "arg.h", "arg.h")


def build(self):
    from cbuild.util import compiler

    cc = compiler.C(self)
    cc.invoke(["ii.c"], "ii", flags=_cflags)


def install(self):
    self.install_bin("ii")
    text = (self.files_path / "ii.1").read_text().replace("VERSION", "1.9")
    (self.cwd / "ii.1.out").write_text(text)
    self.install_man("ii.1.out", name="ii", cat=1)
    self.install_license(self.files_path / "LICENSE")
