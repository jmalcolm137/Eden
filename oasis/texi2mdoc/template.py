pkgname = "texi2mdoc"
pkgver = "0.1.2"
pkgrel = 0
pkgdesc = "TeXinfo to mdoc converter"
license = "ISC"
url = "http://mandoc.bsd.lv/texi2mdoc"
# upstream snapshots host is unreliable; use the source mirror with the same file
source = f"https://sources.voidlinux.org/texi2mdoc-{pkgver}/texi2mdoc-{pkgver}.tgz"
sha256 = "7a45fd87c27cc8970a18db9ddddb2f09f18b8dd5152bf0ca377c3a5e7d304bfe"
# no test suite in the Oasis recipe
options = ["!check"]

_cflags = ["-D__BEGIN_DECLS=", "-D__END_DECLS=", "-Wall"]


def build(self):
    from cbuild.util import compiler

    cc = compiler.C(self)
    cc.invoke(["main.c", "util.c"], "texi2mdoc", flags=_cflags)


def install(self):
    self.install_bin("texi2mdoc")
    self.install_man("texi2mdoc.1")
    self.install_license(self.files_path / "LICENSE")
