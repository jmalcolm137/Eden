pkgname = "grep"
pkgver = "3.12"
pkgrel = 0
build_style = "gnu_configure"
configure_gen = []
pkgdesc = "GNU grep, autoconf compatible"
license = "GPL-3.0-or-later"
url = "https://www.gnu.org/software/grep"
source = f"$(GNU_SITE)/grep/grep-{pkgver}.tar.xz"
sha256 = "2649b27c0e90e632eadcd757be06c6e9a4f48d941de51e7c0f83ff76408a07b9"
# no tests; keep the bootstrap build fast
options = ["!check"]
