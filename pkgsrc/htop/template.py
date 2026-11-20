pkgname = "htop"
pkgver = "3.5.3"
pkgrel = 1
build_style = "gnu_configure"
configure_args = [
    "--with-curses=curses",
    "--disable-hwloc",
    "--disable-capabilities",
    "--disable-delayacct",
    "--disable-sensors",
    "--without-libunwind",
]
configure_env = {
    "CURSES_CFLAGS": "-I.. -I/usr/include",
    "CURSES_LIBS": "/usr/lib/libcurses.a /usr/lib/libterminfo.a",
}
configure_gen = []
makedepends = ["netbsd-curses-devel", "netbsd-curses-devel-static"]
depends = ["netbsd-curses"]
pkgdesc = "Interactive process viewer"
license = "GPL-2.0-or-later"
url = "https://htop.dev"
source = f"https://github.com/htop-dev/htop/releases/download/{pkgver}/htop-{pkgver}.tar.xz"
sha256 = "a8b164386494cb85bb255a415a3f5f80afe7a0c4491da5d113b3a0f951087e65"
tool_flags = {
    # static netbsd-curses libraries, fully self-contained PIE
    "LDFLAGS": ["-static-pie", "-unwindlib=none"],
}
# no automated test suite
options = ["!check"]


def pre_configure(self):
    self.cp(self.files_path / "ncurses.h", "ncurses.h")


def post_install(self):
    # CLI tool; no application icon needed
    self.uninstall("usr/share/pixmaps", missing_ok=True)
