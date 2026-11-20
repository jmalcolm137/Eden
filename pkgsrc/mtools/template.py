pkgname = "mtools"
pkgver = "4.0.48"
pkgrel = 0
build_style = "gnu_configure"
configure_args = ["--disable-floppyd"]
configure_gen = []
pkgdesc = "Utilities for MS-DOS filesystems"
license = "GPL-3.0-or-later"
url = "https://www.gnu.org/software/mtools"
source = f"$(GNU_SITE)/mtools/mtools-{pkgver}.tar.gz"
sha256 = "88f273c6629ad5464482e98a9980727f585eead8736c50717c95e36f05ca05dc"
# no test suite in the package
options = ["!check"]
