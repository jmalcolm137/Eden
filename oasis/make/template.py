pkgname = "make"
pkgver = "4.4.1"
pkgrel = 1
build_style = "gnu_configure"
configure_args = ["--disable-nls"]
configure_gen = []
pkgdesc = "GNU make build tool"
license = "GPL-3.0-or-later"
url = "https://www.gnu.org/software/make"
source = f"{url}/make-{pkgver}.tar.gz"
sha256 = "dd16fb1d67bfab79a72f5e8390735c49e3e8e70b4945a15ab1f81ddb78658fb3"
# no test suite in the Oasis recipe
options = ["!check"]
