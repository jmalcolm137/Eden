pkgname = "python-pexpect"
pkgver = "4.9.0"
pkgrel = 3
hostmakedepends = ["python"]
depends = ["python", "python-ptyprocess"]
pkgdesc = "Python port of expect(1) for child process handling"
license = "ISC"
url = "https://pexpect.readthedocs.io/en/stable"
source = "https://files.pythonhosted.org/packages/source/p/pexpect/pexpect-4.9.0.tar.gz"
sha256 = "ee7d41123f3c9911050ea2c2dac107568dc43b2d3b0c7557a33212c398ead30f"
# pure python
options = ["!check"]


def build(self):
    pass


def install(self):
    self.install_files("pexpect", "usr/lib/python3.15/site-packages")
    self.install_license("LICENSE")
