pkgname = "patch"
pkgver = "2.8.1"
pkgrel = 0
build_style = "gnu_configure"
configure_gen = []
pkgdesc = "GNU patch"
license = "GPL-3.0-or-later"
url = "https://www.gnu.org/software/patch"
source = f"$(GNU_SITE)/patch/patch-{pkgver}.tar.xz"
sha256 = "3240c7959c5347c8ed347e3c4201c0337bf4240d5cf09d68889e58eeaba30e17"
# no tests; keep the bootstrap build fast
options = ["bootstrap", "!check"]
