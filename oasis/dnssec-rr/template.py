pkgname = "dnssec-rr"
pkgver = "0.2"
pkgrel = 0
# Oasis pkg/dnssec-rr/src
_commit = "1c9796ac0b00d786a86dfcb4bd3f5e310e75b324"
makedepends = ["bearssl-devel", "bearssl-devel-static"]
pkgdesc = "DNSSEC record utilities"
license = "ISC"
url = "https://git.sr.ht/~mcf/dnssec-rr"
source = f"{url}/archive/{_commit}.tar.gz"
sha256 = "db0fd65f63040a3aca97d7e51312a8c895e6c22fc04beec76d7824b79050ac38"
# no test suite in the Oasis recipe
options = ["!check"]

_cflags = ["-std=c11", "-Wall", "-Wpedantic", "-D_POSIX_C_SOURCE=200809L"]

_lib_sources = ["base16.c", "base64.c", "dnssec.c", "key.c", "zone.c"]
_tools = ["ds", "dnskey", "nsec", "rrsig", "tlsa"]


def build(self):
    from cbuild.util import compiler

    cc = compiler.C(self)
    self.mkdir("obj", parents=True)
    objs = []
    for src in _lib_sources:
        obj = "obj/" + src.removesuffix(".c") + ".o"
        cc.invoke([src], obj, obj_file=True, flags=_cflags)
        objs.append(obj)
    self.do("ar", "rcs", "libcommon.a", *objs)

    for tool in _tools:
        cc.invoke(
            [f"{tool}.c", "libcommon.a"],
            tool,
            flags=_cflags,
            ldflags=["/usr/lib/libbearssl.a"],
        )


def install(self):
    for tool in _tools:
        self.install_bin(tool)
        self.install_man(f"{tool}.1")
    self.install_license("LICENSE")
