pkgname = "python-packaging"
pkgver = "26.3"
pkgrel = 0
hostmakedepends = ["python"]
depends = ["python"]
pkgdesc = "Core utilities for Python packages"
license = "Apache-2.0 OR BSD-2-Clause"
url = "https://github.com/pypa/packaging"
source = "https://files.pythonhosted.org/packages/7d/fa/3944b40b07da9ce895c0e6303a5ab7d53da063554f534556b134a54d6093/packaging-26.3.tar.gz"
sha256 = "94edc256424af38762eb31306eed28beb9f0efc50a8837492c9d6fd6004aed79"
# pure python
options = ["!check"]


def build(self):
    pass


def install(self):
    self.install_files("src/packaging", "usr/lib/python3.15/site-packages")
    self.install_license("LICENSE")
