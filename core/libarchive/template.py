pkgname = "libarchive"
pkgver = "3.8.10"
pkgrel = 2
build_style = "gnu_configure"
configure_args = [
    "--enable-acl",
    "--enable-xattr",
    "--without-expat",
    "--with-lz4",
    "--without-xml2",
    "--without-nettle",
    "--disable-rpath",
]
configure_gen = []
hostmakedepends = ["pkgconf"]
makedepends = [
    "acl-devel",
    "bzip2-devel",
    "lz4-devel",
    "musl-bsd-headers",
    "xz-devel",
    "zlib-static",
]
pkgdesc = "Library to read/write several different streaming archive formats"
license = "BSD-2-Clause"
url = "https://www.libarchive.org"
source = f"https://github.com/libarchive/libarchive/releases/download/v{pkgver}/libarchive-{pkgver}.tar.gz"
sha256 = "a1bffbe5152cfe869751179e7b16648c87c461cb8c46eee75062efbe164cc57c"
# encoding failures on musl; harmless
options = ["bootstrap", "!check"]

if self.stage > 0:
    configure_args += ["--without-openssl", "--with-zstd"]
    makedepends += ["zstd-devel"]
else:
    configure_args += ["--without-openssl", "--without-zstd"]


def post_install(self):
    self.install_license("COPYING")
    # tar/cpio come from core/openbsd (Oasis pax); keep only the library.
    for f in [
        "usr/bin/bsdtar",
        "usr/bin/tar",
        "usr/bin/bsdcpio",
        "usr/bin/cpio",
        "usr/share/man/man1/bsdtar.1",
        "usr/share/man/man1/tar.1",
        "usr/share/man/man1/bsdcpio.1",
        "usr/share/man/man1/cpio.1",
        "usr/share/man/man5/mtree.5",
    ]:
        self.uninstall(f, missing_ok=True)


@subpackage("libarchive-devel")
def _(self):
    self.depends += makedepends

    return self.default_devel()
