pkgname = "pcre2"
pkgver = "10.49"
pkgrel = 0
build_style = "gnu_configure"
configure_args = [
    "--disable-symvers",
    "--enable-jit",
    "--enable-pcre2-16",
    "--enable-pcre2-32",
    "--enable-static",
    "--with-pic",
]
configure_gen = []
hostmakedepends = ["pkgconf"]
pkgdesc = "Perl Compatible Regular Expressions v2"
license = "BSD-3-Clause"
url = "https://www.pcre.org"
source = "https://github.com/PCRE2Project/pcre2/releases/download/pcre2-10.49/pcre2-10.49.tar.gz"
sha256 = "929f0b20e62879252a15886b06c89f1edef61a363cbd5826fb041080a5e557ae"
# tests need the full upstream test set
options = ["!check"]


def post_install(self):
    self.install_license("LICENCE.md")


@subpackage("pcre2-devel")
def _(self):
    return self.default_devel()
