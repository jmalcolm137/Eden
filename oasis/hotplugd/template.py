pkgname = "hotplugd"
pkgver = "0_git20200101"
pkgrel = 0
# Oasis pkg/hotplugd/src
_commit = "c15eea9bdeb974f828b6eda37f5f24a2420bd7e1"
makedepends = ["linux-headers"]
pkgdesc = "Simple hotplug daemon"
license = "ISC"
url = "https://github.com/oasislinux/hotplugd"
source = f"{url}/archive/{_commit}.tar.gz"
sha256 = "8430e357be4d6240de08f0c8b45a6929450bdc2fdfa6bc531533e61425a6a7ee"
# no test suite in the Oasis recipe
options = ["!check"]

_cflags = [
    "-std=c11",
    "-Wall",
    "-Wextra",
    "-Wpedantic",
    '-DPREFIX="/usr"',
]


def build(self):
    from cbuild.util import compiler

    cc = compiler.C(self)
    cc.invoke(["hotplugd.c"], "hotplugd", flags=_cflags)
    cc.invoke(["ata_id.c"], "ata_id", flags=_cflags)
    cc.invoke(["trigger.c"], "trigger", flags=_cflags)


def install(self):
    self.install_bin("hotplugd")
    self.install_file("ata_id", "usr/lib/hotplugd", mode=0o755)
    self.install_file("trigger", "usr/lib/hotplugd", mode=0o755)
    self.install_license("LICENSE")
