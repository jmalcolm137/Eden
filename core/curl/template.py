pkgname = "curl"
pkgver = "8.20.0"
pkgrel = 4
# Oasis pkg/curl/src
_commit = "291c75968e8551a15fe0d3a4418c5db236c46c4b"
makedepends = ["bearssl-devel", "linux-headers", "zlib-ng-compat-devel", "zlib-ng-compat-devel-static"]
pkgdesc = "URL transfer library and tool from Oasis"
license = "curl"
url = "https://curl.se"
source = f"https://github.com/oasislinux/curl/archive/{_commit}.tar.gz"
sha256 = "2e1b471df3ec4ab20e8de3254258a5aeb159b373ae29588694ca1e7100943f1c"
# no test suite
options = ["bootstrap", "!check", "!lto"]


def _read_list(self, name):
    return [
        line.strip()
        for line in (self.files_path / name).read_text().splitlines()
        if line.strip()
    ]


def pre_build(self):
    self.cp(self.files_path / "curl_config.h", "curl_config.h")
    # Oasis's sha512-256 patch needs a BearSSL with SHA-512/256 support,
    # which the core BearSSL package in this tree does not carry.


def build(self):
    from cbuild.util import compiler

    cc = compiler.C(self)
    flags = [
        "-std=c99",
        "-Wall",
        "-Wpedantic",
        "-Wno-maybe-uninitialized",
        "-D_GNU_SOURCE",
        "-DHAVE_CONFIG_H",
        "-DBUILDING_LIBCURL",
        "-DCURL_STATICLIB",
        "-I.",
        "-Iinclude",
        "-Iinclude/curl",
        "-Ilib",
        "-Ilib/curlx",
        "-Isrc",
    ]
    self.mkdir("obj/lib", parents=True)
    self.mkdir("obj/src", parents=True)

    lib_objs = []
    for src in _read_list(self, "curl-lib.txt"):
        obj = "obj/lib/" + src.removeprefix("lib/").replace("/", "_").removesuffix(".c") + ".o"
        cc.invoke([src], obj, obj_file=True, flags=flags)
        lib_objs.append(obj)
    self.do("ar", "rcs", "libcurl.a", *lib_objs)

    tool_objs = []
    for src in _read_list(self, "curl-tool.txt"):
        obj = "obj/src/" + src.removeprefix("src/").replace("/", "_").removesuffix(".c") + ".o"
        cc.invoke([src], obj, obj_file=True, flags=flags)
        tool_objs.append(obj)

    cc.invoke(
        tool_objs,
        "curl",
        ldflags=["libcurl.a", "-lbearssl", "-lz", "-lm", "-ldl", "-lpthread"],
    )


def install(self):
    self.install_bin("curl")
    self.install_file("libcurl.a", "usr/lib")
    for h in sorted((self.cwd / "include/curl").glob("*.h")):
        self.install_file(f"include/curl/{h.name}", "usr/include/curl")
    self.install_man("docs/cmdline-opts/curl.1")
    self.install_license("COPYING")
