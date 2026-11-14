pkgname = "binutils"
pkgver = "2.46.0"
pkgrel = 1
build_style = "gnu_configure"
configure_args = [
    "--disable-nls",
    "--disable-werror",
    "--disable-gdb",
    "--disable-gprofng",
    "--disable-gold",
    "--disable-multilib",
    "--disable-sim",
    "--disable-libdecnumber",
    "--with-system-zlib",
]
configure_gen = []
make_build_env = {"MAKEINFO": "true"}
make_install_env = {"MAKEINFO": "true"}
makedepends = ["linux-headers", "zlib-ng-compat-devel"]
pkgdesc = "GNU binary utilities"
license = "GPL-3.0-or-later"
url = "https://www.gnu.org/software/binutils"
source = f"https://ftp.gnu.org/gnu/binutils/binutils-{pkgver}.tar.xz"
sha256 = "d75a94f4d73e7a4086f7513e67e439e8fcdcbb726ffe63f4661744e6256b2cf2"
# no test suite in the Oasis recipe
options = ["hardlinks", "!lto", "!check"]
