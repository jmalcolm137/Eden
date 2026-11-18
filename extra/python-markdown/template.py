pkgname = "python-markdown"
pkgver = "3.10.2"
pkgrel = 1
hostmakedepends = ["python"]
depends = ["python"]
pkgdesc = "Python implementation of Markdown"
license = "BSD-3-Clause"
url = "https://github.com/Python-Markdown/markdown"
source = "https://files.pythonhosted.org/packages/source/M/Markdown/markdown-3.10.2.tar.gz"
sha256 = "994d51325d25ad8aa7ce4ebaec003febcce822c3f8c911e3b17c52f7f589f950"
# pure python
options = ["!check"]


def build(self):
    pass


def install(self):
    self.install_files("markdown", "usr/lib/python3.15/site-packages")
    self.install_license("LICENSE.md")
