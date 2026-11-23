pkgname = "libxml2"
pkgver = "2.15.4"
pkgrel = 0
build_style = "gnu_configure"
configure_args = [
    "--enable-shared",
    "--enable-static",
    "--with-legacy",
    "--with-threads",
    "--without-docs",
    "--without-icu",
    "--without-lzma",
    "--without-python",
    "--without-readline",
    "--without-history",
]
configure_gen = []
hostmakedepends = ["pkgconf"]
makedepends = ["zlib"]
pkgdesc = "XML parsing library"
license = "MIT"
url = "http://www.xmlsoft.org"
source = f"https://download.gnome.org/sources/libxml2/{pkgver[: pkgver.rfind('.')]}/libxml2-{pkgver}.tar.xz"
sha256 = "98087fd181d9070724f3fbc65c7377db03038eb92bd882374daff44940138821"


def post_install(self):
    self.install_license("Copyright")


@subpackage("libxml2-devel")
def _(self):
    return self.default_devel()


@subpackage("libxml2-progs")
def _(self):
    return self.default_progs()
