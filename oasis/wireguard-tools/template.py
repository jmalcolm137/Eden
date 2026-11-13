pkgname = "wireguard-tools"
pkgver = "1.0.20260223"
pkgrel = 1
_commit = "49ce333da02056ae7b22ee2aeb6afe8aaed79b19"
makedepends = ["linux-headers"]
pkgdesc = "WireGuard userspace tools"
license = "GPL-2.0-only"
url = "https://www.wireguard.com"
source = f"https://git.zx2c4.com/wireguard-tools/snapshot/wireguard-tools-{pkgver}.tar.xz"
sha256 = "af459827b80bfd31b83b08077f4b5843acb7d18ad9a33a2ef532d3090f291fbf"
# no test suite in the Oasis recipe
options = ["!check"]

_cflags = [
    "-std=gnu99",
    "-Wall",
    "-D_GNU_SOURCE",
    '-DRUNSTATEDIR="/run"',
    "-Isrc/uapi/linux",
]


def build(self):
    from cbuild.util import compiler

    cc = compiler.C(self)
    cc.invoke(
        [
            "src/config.c",
            "src/curve25519.c",
            "src/encoding.c",
            "src/genkey.c",
            "src/ipc.c",
            "src/pubkey.c",
            "src/set.c",
            "src/setconf.c",
            "src/show.c",
            "src/showconf.c",
            "src/terminal.c",
            "src/wg.c",
        ],
        "wg",
        flags=_cflags,
    )


def install(self):
    self.install_bin("wg")
    self.install_man("src/man/wg.8")
    self.install_license("COPYING")
