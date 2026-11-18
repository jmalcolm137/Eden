pkgname = "python-markupsafe"
pkgver = "3.0.3"
pkgrel = 1
hostmakedepends = ["python"]
depends = ["python"]
pkgdesc = "XML/HTML/XHTML markup safe string for Python"
license = "BSD-3-Clause"
url = "https://palletsprojects.com/p/markupsafe"
source = "https://files.pythonhosted.org/packages/source/M/MarkupSafe/markupsafe-3.0.3.tar.gz"
sha256 = "722695808f4b6457b320fdc131280796bdceb04ab50fe1795cd540799ebe1698"
# pure python fallback; the optional speedup extension is not needed
options = ["!check"]


def build(self):
    pass


def install(self):
    self.install_files("src/markupsafe", "usr/lib/python3.15/site-packages")
    self.install_license("LICENSE.txt")
