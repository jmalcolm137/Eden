pkgname = "libpciaccess"
pkgver = "0.18"
pkgrel = 0
# Oasis pkg/libpciaccess/src
_commit = "04271a93ed65bfde82469509120214424eb918d0"
build_style = "meson"
configure_args = ["-Dzlib=disabled", "-Dpci-ids=pci.ids"]
pkgdesc = "Generic PCI access library"
license = "MIT"
url = "https://gitlab.freedesktop.org/xorg/lib/libpciaccess"
source = (
    f"{url}/-/archive/{_commit}/libpciaccess-{_commit}.tar.gz"
)
sha256 = "ee2905e00651fdbabddc60d5a7c439f31fe8bd86d1dcb97ba7ba6d3b784fc725"
# no test suite in the Oasis recipe
options = ["!check"]


def post_install(self):
    self.install_license("COPYING")


@subpackage("libpciaccess-devel")
def _(self):
    return self.default_devel()

