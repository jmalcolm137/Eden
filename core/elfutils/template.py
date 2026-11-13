pkgname = "elfutils"
pkgver = "0.193"
pkgrel = 0
build_style = "gnu_configure"
configure_args = [
    "--disable-nls",
    "--disable-werror",
    "--disable-debuginfod",
    "--disable-libdebuginfod",
    "--enable-deterministic-archives",
    "--with-zstd",
]
# use the generated configure from the release tarball
configure_gen = []
hostmakedepends = ["m4", "pkgconf"]
makedepends = [
    "argp-standalone",
    "bzip2-devel",
    "linux-headers",
    "musl-bsd-headers",
    "musl-fts",
    "musl-obstack",
    "xz-devel",
    "zlib-ng-compat-devel",
    "zstd-devel",
]
pkgdesc = "Utilities and libraries to handle ELF files and DWARF data"
license = "GPL-3.0-or-later AND (GPL-2.0-or-later OR LGPL-3.0-or-later)"
url = "https://sourceware.org/elfutils"
source = (
    f"https://sourceware.org/elfutils/ftp/{pkgver}/elfutils-{pkgver}.tar.bz2"
)
sha256 = "7857f44b624f4d8d421df851aaae7b1402cfe6bcdd2d8049f15fc07d3dde7635"
tool_flags = {
    "CFLAGS": ["-D_GNU_SOURCE", "-Wno-unaligned-access"],
    "LDFLAGS": ["-Wl,-z,stack-size=2097152"],
}
# no test suite, and avoid pulling in bash
options = ["!check"]


def post_build(self):
    self.ln_s("eustack", "build/src/stack")


def post_install(self):
    self.rename("usr/bin/eu-eustack", "eu-stack")


@subpackage("elfutils-libs")
def _(self):
    pv = pkgver[2:]
    self.provides = [
        f"so:libasm.so.1={pv}",
        f"so:libdw.so.1={pv}",
        f"so:libelf.so.1={pv}",
    ]

    return self.default_libs(extra=[f"usr/lib/*-{pkgver}.so"])


@subpackage("elfutils-devel")
def _(self):
    return self.default_devel()
