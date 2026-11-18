pkgname = "libxkbcommon"
pkgver = "1.13.2"
pkgrel = 1
build_style = "meson"
configure_args = [
    "-Denable-bash-completion=false",
    "-Denable-cool-uris=false",
    "-Denable-docs=false",
    "-Denable-tools=false",
    "-Denable-wayland=false",
    "-Denable-x11=false",
    "-Denable-xkbregistry=true",
]
hostmakedepends = [
    "muon",
    "pkgconf",
    "samurai",
]
makedepends = ["libxml2-devel"]
depends = [
    "xkeyboard-config",
]
pkgdesc = "Keyboard handling library"
license = "MIT"
url = "https://xkbcommon.org"
source = "https://github.com/xkbcommon/libxkbcommon/archive/xkbcommon-1.13.2.tar.gz"
sha256 = "acc4d5f7c3cbba5f9f8d08d8bdbeede84ecede46792f47929aa9321873385528"
# tests require a display or a full graphics stack
options = ["!check", "!splitstatic"]


@subpackage("libxkbcommon-devel")
def _(self):
    return self.default_devel()


def post_patch(self):
    # parser.c/h are pre-generated with bison 3.8.2 and tracked in
    # files/ (see files/xkbcommon.patch); use them directly instead
    # of running bison at build time
    for f in ("parser.c", "parser.h"):
        self.cp(self.files_path / f, f"src/xkbcomp/{f}")
    mf = self.cwd / "meson.build"
    mtext = mf.read_text()
    old_bison = "bison = find_program('bison', 'win_bison', required: true, version: '>= 3.6')"
    assert old_bison in mtext
    mtext = mtext.replace(
        old_bison, "bison = find_program('bison', 'win_bison', required: false)"
    )
    old_gen = "    yacc_gen.process('src/xkbcomp/parser.y'),"
    assert old_gen in mtext
    mtext = mtext.replace(old_gen, "    'src/xkbcomp/parser.c',")
    mf.write_text(mtext)


def post_install(self):
    self.install_license("LICENSE")
