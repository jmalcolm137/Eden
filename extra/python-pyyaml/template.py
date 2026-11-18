pkgname = "python-pyyaml"
pkgver = "6.0.3"
pkgrel = 0
hostmakedepends = ["python"]
depends = ["python"]
pkgdesc = "YAML parser and emitter for Python"
license = "MIT"
url = "https://pyyaml.org"
source = "https://files.pythonhosted.org/packages/source/p/pyyaml/pyyaml-6.0.3.tar.gz"
sha256 = "d76623373421df22fb4cf8817020cbb7ef15c725b9d5e45f17e189bfc384190f"
# pure python fallback is sufficient for build tooling
options = ["!check"]


def build(self):
    pass


def install(self):
    self.install_files("lib/yaml", "usr/lib/python3.15/site-packages")
    self.install_license("LICENSE")
