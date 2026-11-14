pkgname = "tz"
pkgver = "2026b"
pkgrel = 0
# Oasis pkg/tz/src
_commit = "48c25a1ba86cb602990c0573aba7795417931bb4"
pkgdesc = "Time zone database and compiler"
license = "custom:public-domain"
url = "https://www.iana.org/time-zones"
source = f"https://github.com/eggert/tz/archive/{_commit}.tar.gz"
sha256 = "f13e0a4da4d03c4be81f603fe9199147c3da0509c79d681b24165b795dca5849"
# no test suite in the Oasis recipe
options = ["!distlicense", "!check"]

_cflags = ["-std=c99", "-Wall", "-Wpedantic", "-Wno-maybe-uninitialized", "-I.", '-DZIC_BLOAT_DEFAULT="slim"']

_zones = [
    "africa",
    "antarctica",
    "asia",
    "australasia",
    "europe",
    "northamerica",
    "southamerica",
    "etcetera",
    "factory",
    "backward",
]


def pre_build(self):
    self.cp(self.files_path / "version.h", "version.h")
    self.cp(self.files_path / "tzdir.h", "tzdir.h")


def build(self):
    from cbuild.util import compiler

    cc = compiler.C(self)
    cc.invoke(["zic.c"], "zic", flags=_cflags)
    self.mkdir("out", parents=True)
    self.do("sh", "-c", "./zic -d out/zoneinfo " + " ".join(_zones))


def install(self):
    self.install_bin("zic")
    self.install_man("zic.8")
    self.install_files("out/zoneinfo", "usr/share", name="zoneinfo")
    for name in ("zone.tab", "zone1970.tab", "iso3166.tab", "leapseconds"):
        if (self.cwd / name).exists():
            self.install_file(name, "usr/share/zoneinfo")
    self.install_license("LICENSE")
