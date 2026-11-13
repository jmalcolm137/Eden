pkgname = "netbsd-curses"
pkgver = "0.1"
pkgrel = 1
build_style = "makefile"
make_build_env = {
    "PREFIX": "/usr",
    "DATADIR": "/usr/share",
    "MANDIR": "/usr/share/man",
}
make_install_env = dict(make_build_env)
make_use_env = True
pkgdesc = "NetBSD curses libraries and tools from Oasis"
license = "BSD-2-Clause AND BSD-3-Clause"
url = "https://github.com/oasislinux/netbsd-curses"
source = f"{url}/archive/e6100a3396a0ac48026985c5bbde76341b895dd7.tar.gz"
sha256 = "94f53617c358a75659c5994567a0c1fe4e976e58679829997b1c477282beaff2"
tool_flags = {"CFLAGS": ["-fPIC"]}
# no tests; upstream only has an interactive regression driver
options = ["!check", "bootstrap"]


def post_install(self):
    self.install_license(self.files_path / "LICENSE")


@subpackage("netbsd-curses-devel")
def _(self):
    return ["usr/include"]


@subpackage("netbsd-curses-devel-static")
def _(self):
    return ["usr/lib/*.a"]
