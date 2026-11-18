pkgname = "nodejs"
pkgver = "26.13.1"
pkgrel = 2
build_style = "configure"
configure_args = [
    "--prefix=/usr",
    # bundled small-icu trims out every ICU break iterator, and V8's
    # Intl.Segmenter then segfaults; the canned full data keeps them
    "--with-intl=full-icu",
    "--openssl-use-def-ca-store",
]
configure_gen = []
hostmakedepends = ["gperf", "perl", "pkgconf", "python"]
makedepends = [
    "libatomic-chimera-devel",
    "libcxx-devel",
    "libunwind-devel",
    "linux-headers",
    "musl-bsd-headers",
]
pkgdesc = "JavaScript runtime built on Chrome's V8 engine"
license = "MIT"
url = "https://nodejs.org"
source = f"{url}/dist/v{pkgver}/node-v{pkgver}.tar.xz"
sha256 = "a7f6204ff63b6a2cd274d48903285abb86ed53a99070e532d4c2fd787457d9e6"
debug_level = 0
hardening = ["!vis", "!cfi"]
# tests require network access
options = ["!check", "!cross", "!lto"]


def post_install(self):
    self.install_license("LICENSE")
