pkgname = "libseccomp"
pkgver = "2.6.2"
pkgrel = 0
build_style = "gnu_configure"
configure_args = ["--disable-static"]
# the release tarball ships a generated configure script
configure_gen = []
hostmakedepends = ["gperf", "pkgconf"]
makedepends = ["linux-headers"]
pkgdesc = "Interface to the Linux kernel's syscall filtering mechanism"
license = "LGPL-2.1-or-later"
url = "https://github.com/seccomp/libseccomp"
source = (
    f"https://github.com/seccomp/libseccomp/releases/download/v{pkgver}/"
    f"libseccomp-{pkgver}.tar.gz"
)
sha256 = "6b845d352c6d7887d8d134c43d86850d40f5dcee11ad1675c18197ae4d869d42"
# the test suite wants valgrind and a full build environment
options = ["!check"]


@subpackage("libseccomp-devel")
def _(self):
    self.depends += ["linux-headers"]
    return self.default_devel()


@subpackage("libseccomp-progs")
def _(self):
    return self.default_progs()
