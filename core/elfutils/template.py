pkgname = "elfutils"
pkgver = "0.193"
pkgrel = 0
build_style = "gnu_configure"
configure_args = [
    "--disable-nls",
    "--disable-debuginfod",
    "--disable-libdebuginfod",
    "--disable-demangler",
    "--disable-werror",
    "--without-bzlib",
    "--without-lzma",
    "--without-zstd",
]
configure_env = {
    "ac_cv_func_fts_close": "yes",
    "ac_cv_func_fts_open": "yes",
    "ac_cv_func_fts_read": "yes",
    "ac_cv_func_fts_set": "yes",
}
configure_gen = []
hostmakedepends = ["pkgconf"]
makedepends = ["argp-standalone", "musl-bsd-headers", "zlib-static"]
pkgdesc = "ELF handling library from elfutils"
license = "GPL-3.0-or-later OR LGPL-3.0-or-later"
url = "https://sourceware.org/elfutils"
source = "https://sourceware.org/elfutils/ftp/0.193/elfutils-0.193.tar.bz2"
sha256 = "7857f44b624f4d8d421df851aaae7b1402cfe6bcdd2d8049f15fc07d3dde7635"
# only the library is built; elfutils tests need the full tree
options = ["!check", "!lto"]


def build(self):
    self.do("gmake", f"-j{self.make_jobs}", "-C", "lib", wrksrc="build")
    self.do("gmake", f"-j{self.make_jobs}", "-C", "libelf", wrksrc="build")


def install(self):
    self.do(
        "gmake",
        "-C",
        "libelf",
        "install",
        f"DESTDIR={self.chroot_destdir}",
        wrksrc="build",
    )


@subpackage("elfutils-devel")
def _(self):
    self.subdesc = "development files"
    return [
        "usr/include/gelf.h",
        "usr/include/libelf.h",
        "usr/include/nlist.h",
        "usr/lib/libelf.a",
        "usr/lib/libelf.so",
    ]
