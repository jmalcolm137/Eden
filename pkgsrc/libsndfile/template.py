pkgname = "libsndfile"
pkgver = "1.2.2"
pkgrel = 1
build_style = "gnu_configure"
configure_args = [
    "--disable-alsa",
    "--disable-external-libs",
    "--disable-full-suite",
    "--disable-sqlite",
]
configure_gen = []
hostmakedepends = ["libtool", "pkgconf", "python"]
pkgdesc = "C library for reading and writing sampled sound files"
license = "LGPL-2.1-or-later"
url = "https://libsndfile.github.io/libsndfile"
source = f"https://github.com/libsndfile/libsndfile/releases/download/{pkgver}/libsndfile-{pkgver}.tar.xz"
sha256 = "3799ca9924d3125038880367bf1468e53a1b7e3686a934f098b7e1d286cdb80e"
# tests need the full upstream corpus
options = ["!check"]


@subpackage("libsndfile-devel")
def _(self):
    return self.default_devel()


def post_install(self):
    self.install_license("COPYING")
