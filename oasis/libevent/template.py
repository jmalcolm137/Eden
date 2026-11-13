pkgname = "libevent"
pkgver = "2.1.12"
pkgrel = 0
build_style = "gnu_configure"
configure_args = [
    "--disable-openssl",
    "--disable-mbedtls",
    "--disable-samples",
    "--disable-libevent-regress",
    "--disable-shared",
    "--enable-static",
]
configure_gen = []
pkgdesc = "Event notification library"
license = "BSD-3-Clause"
url = "https://libevent.org"
source = (
    "https://github.com/libevent/libevent/releases/download/"
    "release-2.1.12-stable/libevent-2.1.12-stable.tar.gz"
)
sha256 = "92e6de1be9ec176428fd2367677e61ceffc2ee1cb119035037a27d346b0403bb"
# no test suite in the Oasis recipe
options = ["!check"]


@subpackage("libevent-devel")
def _(self):
    return ["usr/include", "usr/lib/pkgconfig"]


@subpackage("libevent-devel-static")
def _(self):
    return ["usr/lib/*.a"]


def pre_configure(self):
    p = self.cwd / "configure"
    p.write_text(p.read_text().replace("2.1.12-stable", "2.1.12"))


def post_install(self):
    self.install_license("LICENSE")

    pc = self.destdir / "usr/lib/pkgconfig/libevent.pc"
    if pc.exists():
        text = pc.read_text().replace("2.1.12-stable", "2.1.12")
        pc.write_text(text)
