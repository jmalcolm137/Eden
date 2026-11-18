pkgname = "python-setuptools"
pkgver = "80.10.2"
pkgrel = 3
hostmakedepends = ["python"]
depends = ["python"]
pkgdesc = "Easily build and distribute Python packages"
license = "MIT"
url = "https://github.com/pypa/setuptools"
source = "https://files.pythonhosted.org/packages/source/s/setuptools/setuptools-80.10.2.tar.gz"
sha256 = "8b0e9d10c784bf7d262c4e5ec5d4ec94127ce206e8738f29a437945fbc219b70"
# pure python
options = ["!check"]


def build(self):
    pass


def install(self):
    dest = "usr/lib/python3.15/site-packages"
    for d in ("setuptools", "pkg_resources", "_distutils_hack"):
        self.install_files(d, dest)
    pth = self.cwd / "distutils-precedence.pth"
    pth.write_text(
        "import _distutils_hack; _distutils_hack.add_shim()\n"
    )
    self.install_file("distutils-precedence.pth", dest)
    self.install_license("LICENSE")
