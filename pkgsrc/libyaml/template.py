pkgname = "libyaml"
pkgver = "0.2.5"
pkgrel = 1
build_style = "gnu_configure"
configure_args = ["--disable-static"]
configure_gen = []
hostmakedepends = ["pkgconf"]
pkgdesc = "YAML 1.1 parser and emitter library"
license = "MIT"
url = "https://pyyaml.org/wiki/LibYAML"
source = f"https://pyyaml.org/download/libyaml/yaml-{pkgver}.tar.gz"
sha256 = "c642ae9b75fee120b2d96c712538bd2cf283228d2337df2cf2988e3c02678ef4"
# no meaningful test suite
options = ["!check"]


@subpackage("libyaml-devel")
def _(self):
    return self.default_devel()


def post_install(self):
    self.install_license("License")
