pkgname = "the_silver_searcher"
pkgver = "2.2.0"
pkgrel = 0
build_style = "gnu_configure"
configure_args = []
configure_gen = []
hostmakedepends = ["pkgconf"]
makedepends = ["pcre-devel", "pcre-devel-static", "xz-devel", "xz-devel-static", "zlib-static"]
pkgdesc = "Code-searching tool similar to ack"
license = "Apache-2.0"
url = "https://geoff.greer.fm/ag"
source = f"https://geoff.greer.fm/ag/releases/the_silver_searcher-{pkgver}.tar.gz"
sha256 = "d9621a878542f3733b5c6e71c849b9d1a830ed77cb1a1f6c2ea441d4b0643170"
tool_flags = {"CFLAGS": ["-D_LARGEFILE64_SOURCE", "-DHAVE_LZMA_H", "-fcommon"]}
# no test suite in the Oasis recipe
options = ["!check"]


def post_install(self):
    self.uninstall("usr/share/zsh", missing_ok=True)
