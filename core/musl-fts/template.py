pkgname = "musl-fts"
pkgver = "1.2.7"
pkgrel = 0
pkgdesc = "Implementation of fts for musl"
license = "BSD-3-Clause"
url = "https://github.com/void-linux/musl-fts"
source = f"{url}/archive/v{pkgver}.tar.gz"
sha256 = "49ae567a96dbab22823d045ffebe0d6b14b9b799925e9ca9274d47d26ff482a6"
# no test suite
options = ["!check", "!lto"]


def pre_build(self):
    (self.cwd / "config.h").write_text(
        "#define HAVE_DECL_MAX 1\n"
        "#define HAVE_DECL_UINTMAX_MAX 1\n"
        "#define HAVE_DIRFD 1\n"
        "#define HAVE_DIRENT_H 1\n"
        "#define HAVE_ERRNO_H 1\n"
        "#define HAVE_FCNTL_H 1\n"
        "#define HAVE_STDLIB_H 1\n"
        "#define HAVE_STRING_H 1\n"
        "#define HAVE_UNISTD_H 1\n"
        "#define HAVE_SYS_PARAM_H 1\n"
        "#define HAVE_SYS_STAT_H 1\n"
    )


def build(self):
    from cbuild.util import compiler

    cc = compiler.C(self)
    cc.invoke(["fts.c"], "fts.o", obj_file=True, flags=["-I.", "-D_GNU_SOURCE"])
    self.do("ar", "rcs", "libfts.a", "fts.o")


def install(self):
    self.install_file("libfts.a", "usr/lib")
    self.install_file("fts.h", "usr/include")
    self.install_license("COPYING")
