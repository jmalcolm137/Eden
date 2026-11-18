pkgname = "flex"
pkgver = "2.6.4"
pkgrel = 2
makedepends = [
    "libatomic-chimera-devel-static",
    "libunwind-devel-static",
    "musl-devel-static",
]
depends = ["m4"]
pkgdesc = "Fast lexical analyser generator"
license = "BSD-2-Clause"
url = "https://github.com/westes/flex"
source = f"{url}/releases/download/v{pkgver}/flex-{pkgver}.tar.gz"
sha256 = "e87aae032bf07c26f85ac0ed3250998c37621d95f8bd748b31f15b33c45ee995"
tool_flags = {"LDFLAGS": ["-static-pie"]}
# no test suite in the Oasis recipe
options = ["bootstrap", "!check"]

_cflags = ["-DHAVE_CONFIG_H", "-I."]

_sources = [
    "src/buf.c",
    "src/ccl.c",
    "src/dfa.c",
    "src/ecs.c",
    "src/filter.c",
    "src/gen.c",
    "src/main.c",
    "src/misc.c",
    "src/nfa.c",
    "src/options.c",
    "src/parse.c",
    "src/regex.c",
    "src/scan.c",
    "src/scanflags.c",
    "src/scanopt.c",
    "src/skel.c",
    "src/sym.c",
    "src/tables.c",
    "src/tables_shared.c",
    "src/tblcmp.c",
    "src/yylex.c",
]


def pre_build(self):
    self.cp(self.files_path / "config.h", "config.h")


def build(self):
    from cbuild.util import compiler

    cc = compiler.C(self)
    cc.invoke(_sources, "flex", flags=_cflags)


def install(self):
    self.install_bin("flex")
    self.install_link("usr/bin/lex", "flex")
    self.install_man("doc/flex.1")
    self.install_license("COPYING")
