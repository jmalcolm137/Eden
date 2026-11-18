pkgname = "libvorbis"
pkgver = "1.3.7"
pkgrel = 1
build_style = "gnu_configure"
configure_args = ["--disable-static"]
configure_gen = []
hostmakedepends = ["pkgconf"]
makedepends = ["libogg-devel"]
pkgdesc = "Vorbis audio codec library"
license = "BSD-3-Clause"
url = "https://www.xiph.org/vorbis"
source = "https://downloads.xiph.org/releases/vorbis/libvorbis-1.3.7.tar.xz"
sha256 = "b33cc4934322bcbf6efcbacf49e3ca01aadbea4114ec9589d1b1e9d20f72954b"
# tests need a large audio corpus
options = ["!check"]


@subpackage("libvorbis-devel")
def _(self):
    return self.default_devel()


def post_install(self):
    self.install_license("COPYING")
