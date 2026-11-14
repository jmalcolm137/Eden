pkgname = "alsa-lib"
pkgver = "1.2.11"
pkgrel = 1
build_style = "gnu_configure"
configure_args = ["--disable-python", "--disable-topology", "--without-versioned"]
configure_gen = []
makedepends = ["linux-headers"]
pkgdesc = "Advanced Linux Sound Architecture library"
license = "LGPL-2.1-or-later"
url = "https://www.alsa-project.org"
source = f"{url}/files/pub/lib/alsa-lib-{pkgver}.tar.bz2"
sha256 = "9f3f2f69b995f9ad37359072fbc69a3a88bfba081fc83e9be30e14662795bb4d"
# no test suite in the Oasis recipe
options = ["!check"]


@subpackage("alsa-lib-devel")
def _(self):
    return self.default_devel()
