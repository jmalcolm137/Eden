pkgname = "pwgen"
pkgver = "2.08"
pkgrel = 0
# Oasis pkg/pwgen/src
_commit = "c25787fce93b2c99efd87219585c0531e80b6d1c"
pkgdesc = "Password generator"
license = "GPL-2.0-or-later"
url = "https://github.com/tytso/pwgen"
source = f"{url}/archive/{_commit}.tar.gz"
sha256 = "6b9d391347680d73a5bf46df562a36ffbe5078f65fa677d0f47d426b4d97dac6"
# no test suite
options = ["!check"]

_cflags = [
    "-std=c99",
    "-Wall",
    "-Wpedantic",
    "-D_POSIX_C_SOURCE=200809L",
]


def build(self):
    from cbuild.util import compiler

    cc = compiler.C(self)
    cc.invoke(
        [
            "pwgen.c",
            "pw_phonemes.c",
            "pw_rand.c",
            "randnum.c",
            "sha1.c",
            "sha1num.c",
        ],
        "pwgen",
        flags=_cflags,
    )


def install(self):
    self.install_bin("pwgen")
    self.install_man("pwgen.1")
