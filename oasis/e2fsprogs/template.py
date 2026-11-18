pkgname = "e2fsprogs"
pkgver = "1.46.4"
pkgrel = 2
build_style = "gnu_configure"
configure_args = [
    "--disable-nls",
    "--disable-defrag",
    "--disable-fuse2fs",
    "--enable-libuuid",
    "--enable-libblkid",
    "--enable-symlink-install",
]
configure_env = {"ac_cv_have_decl_lseek64": "yes", "ac_cv_func_lseek64": "yes"}
configure_gen = []
hostmakedepends = ["pkgconf"]
makedepends = ["linux-headers"]
pkgdesc = "Ext2/3/4 filesystem utilities"
license = "GPL-2.0-or-later AND LGPL-2.1-or-later"
url = "https://e2fsprogs.sourceforge.net"
source = f"https://www.kernel.org/pub/linux/kernel/people/tytso/e2fsprogs/v{pkgver}/e2fsprogs-{pkgver}.tar.gz"
sha256 = "a30422ea202eccf6267fc920a11e5777b1bf8287de71c4524a8ca539d44e8b55"
# no test suite in the Oasis recipe
options = ["etcfiles", "!check"]


def pre_install(self):
    for d in (
        "etc",
        "usr/include/et",
        "usr/include/e2p",
        "usr/include/ss",
        "usr/include/com_err",
        "usr/include/ext2fs",
        "usr/include/uuid",
        "usr/include/blkid",
        "usr/lib",
        "usr/lib/pkgconfig",
        "usr/share/et",
        "usr/share/ss",
        "usr/share/doc",
        "usr/share/man/man1",
        "usr/share/man/man3",
        "usr/share/man/man5",
        "usr/share/man/man8",
        "usr/share/info",
    ):
        self.install_dir(d)


@subpackage("e2fsprogs-devel")
def _(self):
    return self.default_devel()
