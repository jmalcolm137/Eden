pkgname = "catgirl"
pkgver = "2.2a"
pkgrel = 0
makedepends = [
    "bearssl-devel-static",
    "libtls-bearssl-devel",
    "libtls-bearssl-devel-static",
    "netbsd-curses-devel",
    "netbsd-curses-devel-static",
]
pkgdesc = "IRC client"
license = "ISC"
url = "https://git.causal.agency/catgirl"
source = "https://git.causal.agency/catgirl/snapshot/catgirl-2.2a.tar.gz"
sha256 = "c6d760aaee134e052586def7a9103543f7281fde6531fbcb41086470794297c2"
# no test suite in the Oasis recipe
options = ["!check"]

_cflags = [
    "-std=c11", "-Wall", "-Wextra", "-Wpedantic",
    "-Wno-maybe-uninitialized", "-D_GNU_SOURCE",
]

_ldflags = [
    "/usr/lib/libtls.a", "/usr/lib/libbearssl.a",
    "/usr/lib/libcurses.a", "/usr/lib/libterminfo.a",
    "-lpthread",
]


def build(self):
    from cbuild.util import compiler

    cc = compiler.C(self)
    cc.invoke(
        ["buffer.c", "chat.c", "command.c", "complete.c", "config.c",
         "edit.c", "filter.c", "handle.c", "input.c", "irc.c", "log.c",
         "ui.c", "url.c", "window.c", "xdg.c", "compat_readpassphrase.c"],
        "catgirl",
        flags=_cflags,
        ldflags=_ldflags,
    )


def install(self):
    self.install_bin("catgirl")
    self.install_man("catgirl.1")
    self.install_license("LICENSE")
