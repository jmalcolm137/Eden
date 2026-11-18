pkgname = "icu"
pkgver = "79.1"
pkgrel = 1
build_style = "gnu_configure"
configure_script = "source/configure"
configure_args = [
    "--disable-extras",
    "--disable-samples",
    "--disable-tests",
    "--with-data-packaging=library",
]
configure_env = {
    "U_MAKE": "gmake",
    "ac_cv_prog_PYTHON": "",
}
configure_gen = []
hostmakedepends = ["pkgconf"]
pkgdesc = "Robust and full-featured Unicode services"
license = "custom:unicode"
url = "https://icu.unicode.org"
source = f"https://github.com/unicode-org/icu/releases/download/release-{pkgver}/icu4c-{pkgver}-sources.tgz"
sha256 = "06fa63ecb521048f8082f12ad988f6b678d90cbd88aafce24cbc94902b191d99"
# tests are not built
options = ["!check"]


@subpackage("icu-devel")
def _(self):
    return self.default_devel()


@subpackage("icu-progs")
def _(self):
    return self.default_progs()


def post_install(self):
    self.install_license("LICENSE")
