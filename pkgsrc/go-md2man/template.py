pkgname = "go-md2man"
pkgver = "2.0.7"
pkgrel = 0
build_style = "go"
make_build_args = ["."]
hostmakedepends = ["go"]
pkgdesc = "Markdown to man page converter"
license = "MIT"
url = "https://github.com/cpuguy83/go-md2man"
source = f"https://github.com/cpuguy83/go-md2man/archive/refs/tags/v{pkgver}.tar.gz"
sha256 = "ca3a5b57e2c01759f5a00ad2a578d034c5370fae9aa7a6c3af5648b2fc802a92"
# no test suite
options = ["!check"]


def install(self):
    self.install_bin(self.cwd / "build" / "go-md2man")
    self.install_license("LICENSE.md")
