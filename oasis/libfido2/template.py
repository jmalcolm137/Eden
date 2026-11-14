pkgname = "libfido2"
pkgver = "1.9.0"
pkgrel = 0
_commit = "328395f410034d93d806bd36c9aa1584d802cd2e"
makedepends = [
    "bearssl-devel-static", "libcbor", "libcbor-devel", "linux-headers",
    "openbsd-devel",
    "openbsd-devel-static", "zlib-ng-compat-devel",
    "zlib-ng-compat-devel-static",
]
pkgdesc = "FIDO2 library"
license = "BSD-2-Clause"
url = "https://github.com/libfido2/libfido2"
source = f"https://github.com/oasislinux/libfido2/archive/{_commit}.tar.gz"
sha256 = "56432bb41896265a087439d4a2164079c4b10224cf4f5e1a754b7edee321964c"
# no test suite in the Oasis recipe
options = ["!check"]

_cflags = [
    "-std=c11", "-Wall", "-Wextra", "-Wpedantic", "-Wno-overflow",
    "-DHAVE__THREAD_LOCAL", "-include", "config.h",
    "-D_GNU_SOURCE", "-D_DEFAULT_SOURCE", "-D_FIDO_INTERNAL",
    "-I.", "-Isrc", "-I/usr/include/openbsd",
]

_libsrc = [
    "src/aes256.c", "src/assert.c", "src/authkey.c", "src/bio.c",
    "src/blob.c", "src/buf.c", "src/cbor.c", "src/compress.c",
    "src/config.c", "src/cred.c", "src/credman.c", "src/dev.c",
    "src/ecdh.c", "src/eddsa.c", "src/err.c", "src/es256.c",
    "src/hid.c", "src/info.c", "src/io.c", "src/iso7816.c",
    "src/largeblob.c", "src/log.c", "src/pin.c", "src/random.c",
    "src/reset.c", "src/rs1.c", "src/rs256.c", "src/time.c",
    "src/tpm.c", "src/types.c", "src/u2f.c",
    "src/hid_linux.c", "src/hid_unix.c",
]

_deps = [
    "/usr/lib/libbearssl.a", "/usr/lib/libcbor.a", "/usr/lib/libbsd.a",
    "/usr/lib/libz.a",
]


def pre_build(self):
    self.cp(self.template_path / "config.h", self.cwd / "config.h")


def build(self):
    from cbuild.util import compiler

    cc = compiler.C(self)
    self.mkdir("obj", parents=True)
    objs = []
    for src in _libsrc:
        obj = "obj/" + src.replace("/", "_") + ".o"
        cc.invoke([src], obj, obj_file=True, flags=_cflags)
        objs.append(obj)
    self.do("ar", "rcs", "libfido2.a", *objs)

    common = []
    for src in ["tools/base64.c", "tools/util.c"]:
        obj = "obj/" + src.replace("/", "_") + ".o"
        cc.invoke([src], obj, obj_file=True, flags=_cflags)
        common.append(obj)
    self.do("ar", "rcs", "libcommon.a", *common)

    cc.invoke([
        "tools/fido2-cred.c", "tools/cred_make.c", "tools/cred_verify.c",
        "libcommon.a", "libfido2.a", *_deps,
    ], "fido2-cred", flags=_cflags)
    cc.invoke([
        "tools/fido2-token.c", "tools/bio.c", "tools/config.c",
        "tools/credman.c", "tools/largeblob.c", "tools/pin.c",
        "tools/token.c", "libcommon.a", "libfido2.a", *_deps,
    ], "fido2-token", flags=_cflags)


def install(self):
    self.install_lib("libfido2.a")
    self.install_lib("libcommon.a")
    self.install_bin("fido2-cred")
    self.install_bin("fido2-token")
    self.install_man("man/fido2-cred.1")
    self.install_man("man/fido2-token.1")
    self.install_file("src/fido.h", "usr/include")
    self.install_dir("usr/include/fido")
    for hdr in ["credman.h", "err.h", "param.h", "types.h"]:
        self.install_file(f"src/fido/{hdr}", "usr/include/fido")
    self.install_license("LICENSE")


@subpackage("libfido2-devel")
def _(self):
    return self.default_devel()
