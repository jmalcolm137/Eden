pkgname = "diffutils"
pkgver = "3.12"
pkgrel = 1
build_style = "gnu_configure"
configure_gen = []
pkgdesc = "GNU diff utilities"
license = "GPL-3.0-or-later"
url = "https://www.gnu.org/software/diffutils"
source = f"$(GNU_SITE)/diffutils/diffutils-{pkgver}.tar.xz"
sha256 = "7c8b7f9fc8609141fdea9cece85249d308624391ff61dedaf528fcb337727dfd"
# no tests; keep the bootstrap build fast
options = ["bootstrap", "!check"]
