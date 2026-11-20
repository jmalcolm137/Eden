pkgname = "xcbproto"
pkgver = "1.17.0"
pkgrel = 0
build_style = "gnu_configure"
configure_args = ["--enable-legacy"]
hostmakedepends = ["automake", "pkgconf", "python"]
depends = ["python"]
pkgdesc = "XML-XCB protocol descriptions"
license = "MIT"
url = "https://xcb.freedesktop.org"
source = f"https://gitlab.freedesktop.org/xorg/proto/xcbproto/-/archive/xcb-proto-{pkgver}/xcbproto-xcb-proto-{pkgver}.tar.gz"
sha256 = "479447448281cfb6585ad780f23bd75311af20daf344fb9209c8a87ea77e296a"
# upstream test suites need a full X session
options = ["!check"]


def post_install(self):
    self.install_license("COPYING")
