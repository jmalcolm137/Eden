pkgname = "sed"
pkgver = "4.10"
pkgrel = 0
build_style = "gnu_configure"
configure_gen = []
makedepends = ["linux-headers"]
pkgdesc = "GNU sed, autoconf compatible"
license = "GPL-3.0-or-later"
url = "https://www.gnu.org/software/sed"
source = f"$(GNU_SITE)/sed/sed-{pkgver}.tar.xz"
sha256 = "b8e72182b2ec96a3574e2998c47b7aaa64cc20ce000d8e9ac313cc07cecf28c7"
# no tests; keep the bootstrap build fast
options = ["!check"]
