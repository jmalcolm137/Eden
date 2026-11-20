pkgname = "binutils"
pkgver = "2.46.0"
pkgrel = 4
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
    "--bindir=/usr/gnubin",
]
configure_gen = []
make_build_env = {"MAKEINFO": "true"}
make_install_env = {"MAKEINFO": "true"}
makedepends = ["linux-headers", "zlib-static"]
pkgdesc = "GNU binary utilities"
license = "GPL-3.0-or-later"
url = "https://www.gnu.org/software/binutils"
source = f"https://ftp.gnu.org/gnu/binutils/binutils-{pkgver}.tar.xz"
sha256 = "d75a94f4d73e7a4086f7513e67e439e8fcdcbb726ffe63f4661744e6256b2cf2"
# no test suite in the Oasis recipe
options = ["hardlinks", "!lto", "!check"]


def pre_configure(self):
    # Build for an Eden target instead of the cports default triplet, so the
    # installed target directory and ld's compiled-in search paths say eden
    # rather than chimera. The tools themselves keep their unprefixed names.
    target = self.profile.triplet.replace("-chimera-", "-eden-")
    self.configure_args.append("--target=" + target)
    self.configure_args.append("--program-transform-name=s/^" + target + "-//")

