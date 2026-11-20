pkgname = "strace"
pkgver = "7.3"
pkgrel = 0
build_style = "gnu_configure"
configure_args = [
    "--enable-stacktrace=no",
    "--enable-mpers=no",
]
configure_gen = []
makedepends = ["linux-headers"]
pkgdesc = "System call tracer"
license = "LGPL-2.1-or-later"
url = "https://strace.io"
source = f"https://github.com/strace/strace/releases/download/v{pkgver}/strace-{pkgver}.tar.xz"
sha256 = "529634c40910895a9a1f3c5c1e65da2ca9ed72fb158dfc4bcc89efdf05e39b72"
# no test suite in the Oasis recipe
options = ["!check"]
