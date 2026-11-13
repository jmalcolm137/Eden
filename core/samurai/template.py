pkgname = "samurai"
pkgver = "1.3.11"
pkgrel = 0
build_style = "makefile"
pkgdesc = "Ninja-compatible build tool from Oasis"
license = "ISC"
url = "https://github.com/michaelforney/samurai"
source = f"{url}/archive/addea50762f69dcf6e0699404e0d7f4ef7a0491f.tar.gz"
sha256 = "5075f80a3bcf5596a71b298c2a57c4c0b2ba31506d54f56207c43162f3fc192e"
# no test suite
options = ["!check", "bootstrap"]


def post_install(self):
    self.install_license("LICENSE")
