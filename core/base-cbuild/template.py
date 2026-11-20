pkgname = "base-cbuild"
pkgver = "0.1"
pkgrel = 29
build_style = "meta"
# musl must be built first to provide shlibs for later packages during stage 0
depends = [
    "apk-tools",
    "argp-standalone",
    "awk",
    "base-files",
    "bearssl",
    "bubblewrap",
    "byacc",
    "bzip2",
    "clang",
    "elfutils-devel",
    "fakeroot-core",
    "flex",
    "git",
    "gmake",
    "gnu-m4",
    "gsed",
    "libressl",
    "linux-headers",
    "linux-personality",
    "lld",
    "llvm",
    "muon",
    "musl-devel",
    "musl-fts",
    "musl-obstack",
    "netbsd-curses",
    "oksh",
    "openbsd",
    "pigz",
    "pkgconf",
    "samurai",
    "sbase",
    "ubase",
    "xz",
    "zlib-static",
    "zstd",
    self.with_pkgver("base-cbuild-progs"),
]
# bootstrap-llvm is temporary until next llvm release, don't feel like rebuild
provides = [
    "bootstrap:cbuild=9999-r0",
    "bootstrap:llvm=9999-r0",
]
replaces = ["apk-tools"]
replaces_priority = 1000
pkgdesc = "Minimal Oasis-composed cbuild container"
license = "custom:meta"
url = "https://oasislinux.org"
options = ["bootstrap", "brokenlinks"]

if self.stage > 0:
    depends += ["apk-tools-static-bin"]

# Chimera Linux inpspired toolchain (clang/llvm/lld, gmake, musl),
# Oasis supplies the userland (sbase, ubase, oksh, base-files).


def build(self):
    from cbuild.util import compiler

    self.cp(self.files_path / "cbuild-cross-cc.c", ".")
    self.cp(self.files_path / "cbuild-lld-wrapper.c", ".")

    cc = compiler.C(self)
    cc.invoke(["cbuild-cross-cc.c"], "cbuild-cross-cc")
    cc.invoke(["cbuild-lld-wrapper.c"], "cbuild-lld-wrapper")


def install(self):
    self.install_bin("cbuild-cross-cc")
    self.install_bin("cbuild-lld-wrapper")

    # replace regular ld and ld.lld symlinks
    self.install_link("usr/bin/ld.lld", "cbuild-lld-wrapper")
    self.install_link("usr/bin/ld64.lld", "cbuild-lld-wrapper")

    # different default apk config
    self.install_file(self.files_path / "config", "usr/lib/apk")


@subpackage("base-cbuild-progs")
def _(self):
    # make sure to use our wrapper symlinks
    self.replaces = ["lld"]
    self.replaces_priority = 100
    self.options = ["!scancmd"]

    return self.default_progs()
