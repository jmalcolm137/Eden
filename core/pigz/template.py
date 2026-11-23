pkgname = "pigz"
pkgver = "2.8"
pkgrel = 2
build_style = "makefile"
makedepends = [
    "libatomic-chimera-devel-static",
    "libunwind-devel-static",
    "musl-devel-static",
    "zlib",
]
pkgdesc = "Parallel gzip, also providing gzip/gunzip/zcat"
license = "Zlib"
url = "https://github.com/madler/pigz"
source = f"https://zlib.net/pigz/pigz-{pkgver}.tar.gz"
sha256 = "eb872b4f0e1f0ebe59c9f7bd8c506c4204893ba6a8492de31df416f0d5170fd0"
tool_flags = {"LDFLAGS": ["-static-pie"]}
# no tests; upstream only has an interactive test target
options = ["!check", "bootstrap"]


def install(self):
    self.install_bin("pigz")
    self.install_bin("unpigz")
    self.install_man("pigz.1")
    self.install_link("usr/share/man/man1/unpigz.1", "pigz.1")
    # cbuild and build systems expect gzip-compatible names.
    for name in ["gzip", "gunzip", "zcat"]:
        self.install_link(f"usr/bin/{name}", "pigz")
        self.install_link(f"usr/share/man/man1/{name}.1", "pigz.1")
