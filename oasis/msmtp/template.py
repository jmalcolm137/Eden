pkgname = "msmtp"
pkgver = "1.8.22"
pkgrel = 0
# Oasis pkg/msmtp/src
_commit = "8ee1b0e42f4a735c547caed35775cfe858e69d40"
makedepends = [
    "bearssl-devel-static",
    "libtls-bearssl-devel",
    "libtls-bearssl-devel-static",
]
pkgdesc = "SMTP client"
license = "GPL-3.0-or-later"
url = "https://marlam.de/msmtp"
source = f"https://github.com/marlam/msmtp-mirror/archive/{_commit}.tar.gz"
sha256 = "648f2a61b56a49312f1d05bbd2949743a24edbf722e22301a9c197dca9c26154"
# no test suite in the Oasis recipe
options = ["!check"]

_cflags = ["-DHAVE_CONFIG_H", '-DSYSCONFDIR="/etc"', "-I."]

_sources = [
    "src/conf.c",
    "src/eval.c",
    "src/list.c",
    "src/md5.c",
    "src/md5-apps.c",
    "src/msgid.c",
    "src/msmtp.c",
    "src/net.c",
    "src/netrc.c",
    "src/readbuf.c",
    "src/smtp.c",
    "src/stream.c",
    "src/tools.c",
    "src/xalloc.c",
    "src/aliases.c",
    "src/password.c",
    "src/base64.c",
    "src/mtls.c",
    "src/mtls-libtls.c",
]


def pre_build(self):
    self.cp(self.files_path / "config.h", "config.h")


def build(self):
    from cbuild.util import compiler

    cc = compiler.C(self)
    cc.invoke(
        _sources,
        "msmtp",
        flags=_cflags,
        ldflags=["/usr/lib/libtls.a", "/usr/lib/libbearssl.a", "-lpthread"],
    )


def install(self):
    self.install_bin("msmtp")
    self.install_man("doc/msmtp.1")
    self.install_license("COPYING")
