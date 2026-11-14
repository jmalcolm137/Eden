pkgname = "awk"
pkgver = "20260426"
pkgrel = 0
build_style = "makefile"
make_build_target = "a.out"
make_build_args = ["YACC=byacc -d -b awkgram", "HOSTCC=clang"]
hostmakedepends = ["byacc"]
pkgdesc = "One True awk from Oasis"
license = "custom:awk"
url = "https://github.com/onetrueawk/awk"
source = f"{url}/archive/refs/tags/{pkgver}.tar.gz"
sha256 = "7ae5b9fc6a8149bc45ea0ba3ba434a69a16d1460d19f6d01b6f04cc885b8e02b"
# no tests; upstream's check target runs a large interactive regression suite
options = ["bootstrap", "!check"]


def install(self):
    self.install_bin("a.out", name="awk")
    self.install_man("awk.1")
    self.install_license("LICENSE")
