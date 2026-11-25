pkgname = "conmon"
pkgver = "2.2.1"
pkgrel = 0
build_style = "makefile"
make_build_args = ["DISABLE_SYSTEMD=1"]
make_install_args = ["GOMD2MAN=go-md2man"]
hostmakedepends = ["bash", "go-md2man", "pkgconf"]
makedepends = ["glib-devel", "libseccomp-devel"]
pkgdesc = "OCI container runtime monitor"
license = "Apache-2.0"
url = "https://github.com/containers/conmon"
source = f"{url}/archive/v{pkgver}/conmon-{pkgver}.tar.gz"
sha256 = "814fb5979a3a4b8576b1f901e606b482bebb41cb7e57926e6d5765ee786b96d3"


def check(self):
    self.do("./bin/conmon", "--version")
