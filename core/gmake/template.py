pkgname = "gmake"
pkgver = "4.4.1"
pkgrel = 7
build_style = "gnu_configure"
configure_args = ["--without-guile"]
configure_gen = []
pkgdesc = "GNU Make build tool"
license = "GPL-3.0-or-later"
url = "http://www.gnu.org/software/make"
source = f"$(GNU_SITE)/make/make-{pkgver}.tar.gz"
sha256 = "dd16fb1d67bfab79a72f5e8390735c49e3e8e70b4945a15ab1f81ddb78658fb3"
hardening = ["!cfi"]
# Local fork: do not install /usr/bin/make. Oasis sbase provides make;
# cbuild is patched to invoke gmake explicitly for GNU make.
# perl needs gmake to build, so tests introduce a cycle
options = ["!check", "bootstrap"]


def post_install(self):
    # GNU make installs itself as bin/make; expose it only as gmake so the
    # Oasis sbase make can remain /usr/bin/make.  The /usr/gnubin name is
    # provided by gnu-compat.
    self.rename("usr/bin/make", "usr/bin/gmake", relative=False)
