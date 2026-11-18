pkgname = "python-ptyprocess"
pkgver = "0.7.0"
pkgrel = 3
hostmakedepends = ["python"]
depends = ["python"]
pkgdesc = "Run subprocesses in pseudo-terminals"
license = "ISC"
url = "https://github.com/pexpect/ptyprocess"
source = "https://files.pythonhosted.org/packages/source/p/ptyprocess/ptyprocess-0.7.0.tar.gz"
sha256 = "5c5d0a3b48ceee0b48485e0c26037c0acd7d29765ca3fbb5cb3831d347423220"
# pure python
options = ["!check"]


def build(self):
    pass


def install(self):
    self.install_files("ptyprocess", "usr/lib/python3.15/site-packages")
    self.install_license("LICENSE")
