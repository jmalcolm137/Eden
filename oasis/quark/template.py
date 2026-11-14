pkgname = "quark"
pkgver = "0_git20200101"
pkgrel = 0
pkgdesc = "Small HTTP server"
license = "ISC"
url = "https://tools.suckless.org/quark"
# source is the Oasis-pinned suckless commit, vendored under files/
options = ["!check"]

_cflags = [
    "-std=c99", "-Wpedantic", "-Wall", "-Wextra",
    "-D_DEFAULT_SOURCE", "-D_XOPEN_SOURCE=700", "-D_BSD_SOURCE",
    "-DVERSION=0", "-I.",
]

_files = [
    "arg.h", "config.h", "connection.c", "connection.h", "data.c", "data.h",
    "http.c", "http.h", "main.c", "queue.c", "queue.h", "server.c",
    "server.h", "sock.c", "sock.h", "util.c", "util.h", "quark.1", "LICENSE",
]

_sources = [
    "main.c", "connection.c", "data.c", "http.c", "queue.c",
    "server.c", "sock.c", "util.c",
]


def pre_build(self):
    for name in _files:
        self.cp(self.files_path / name, name)


def build(self):
    from cbuild.util import compiler

    cc = compiler.C(self)
    cc.invoke(_sources, "quark", flags=_cflags)


def install(self):
    self.install_bin("quark")
    self.install_man("quark.1")
    self.install_license("LICENSE")
