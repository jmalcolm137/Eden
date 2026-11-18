pkgname = "fribidi"
pkgver = "1.0.16"
pkgrel = 2
build_style = "meson"
configure_args = ["-Ddocs=false"]
hostmakedepends = [
    "muon",
    "pkgconf",
    "samurai",
]
makedepends = [
    "libatomic-chimera-devel-static",
    "libunwind-devel-static",
    "musl-devel-static",
]
pkgdesc = "Free implementation of the Unicode Bidirectional Algorithm"
license = "LGPL-2.1-or-later"
url = "https://github.com/fribidi/fribidi"
source = "https://github.com/fribidi/fribidi/archive/v1.0.16.tar.gz"
sha256 = "5a1d187a33daa58fcee2ad77f0eb9d136dd6fa4096239199ba31e850d397e8a8"
# tests require a display
options = ["!check"]


@subpackage("fribidi-devel")
def _(self):
    return self.default_devel()


def post_build(self):
    # Keep the shared lib for consumers, but link the tool statically.
    from cbuild.util import compiler

    cc = compiler.C(self)
    cc.invoke(
        ["bin/fribidi-main.c"],
        "fribidi-static",
        flags=["-DHAVE_CONFIG_H", "-I.", "-Ilib", "-Ibuild", "-Ibuild/lib", "-Ibuild/gen.tab"],
        ldflags=["build/lib/libfribidi.a", "-lm", "-static-pie"],
    )


def post_install(self):
    self.install_license("COPYING")
    self.uninstall("usr/bin/fribidi")
    self.install_bin("fribidi-static", name="fribidi")
