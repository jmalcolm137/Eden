pkgname = "python-mako"
pkgver = "1.3.10"
pkgrel = 1
hostmakedepends = ["python"]
depends = ["python", "python-markupsafe"]
pkgdesc = "Fast and lightweight templating engine for Python"
license = "MIT"
url = "https://www.makotemplates.org"
source = "https://files.pythonhosted.org/packages/source/M/Mako/mako-1.3.10.tar.gz"
sha256 = "99579a6f39583fa7e5630a28c3c1f440e4e97a414b80372649c0ce338da2ea28"
# pure python
options = ["!check"]


def build(self):
    pass


def install(self):
    self.install_files("mako", "usr/lib/python3.15/site-packages")
    self.install_license("LICENSE")
