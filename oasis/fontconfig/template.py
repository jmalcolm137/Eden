pkgname = "fontconfig"
pkgver = "2.13.1"
pkgrel = 0
build_style = "gnu_configure"
configure_args = ["--disable-docs", "--disable-shared", "--enable-static"]
configure_env = {
    "UUID_CFLAGS": "-I/usr/include",
    "FREETYPE_CFLAGS": "-I/usr/include/freetype2",
    "FREETYPE_LIBS": "-L/usr/lib -lfreetype",
    "UUID_LIBS": "-L/usr/lib -luuid",
}
configure_gen = []
make_build_args = [
    "SUBDIRS=fontconfig fc-case fc-lang src fc-cache fc-cat fc-conflist "
    "fc-list fc-match fc-pattern fc-query fc-scan fc-validate conf.d its po po-conf"
]
make_install_args = [
    "SUBDIRS=fontconfig fc-case fc-lang src fc-cache fc-cat fc-conflist "
    "fc-list fc-match fc-pattern fc-query fc-scan fc-validate conf.d its po po-conf"
]
makedepends = [
    "e2fsprogs-devel",
    "e2fsprogs-devel-static",
    "expat",
    "freetype",
    "gperf",
    "zlib-static",
]
pkgdesc = "Font configuration and customisation library"
license = "MIT"
url = "https://www.freedesktop.org/wiki/Software/fontconfig"
source = (
    "https://www.freedesktop.org/software/fontconfig/release/"
    f"fontconfig-{pkgver}.tar.gz"
)
sha256 = "9f0d852b39d75fc655f9f53850eb32555394f36104a044bb2b2fc9e66dbbfa7f"
# no test suite in the Oasis recipe
options = ["etcfiles", "!check"]


def pre_build(self):
    self.cp(self.files_path / "fcobjshash.h", "build/fcobjshash.h")
    (self.cwd / "build/fcobjshash.h").touch()
    p = self.cwd / "build/fcobjshash.gperf"
    if not p.exists():
        p.write_text("")
    p.touch()
    stamp = self.cwd / "build/stamp-fcobjshash.gperf"
    stamp.write_text("")
    stamp.touch()

    for mk in (self.cwd / "build").glob("fc-*/Makefile"):
        text = mk.read_text()
        text = text.replace(
            "${top_builddir}/src/libfontconfig.la",
            "${top_builddir}/src/libfontconfig.la /usr/lib/libz.a",
        )
        text = text.replace(
            "$(top_builddir)/src/libfontconfig.la",
            "$(top_builddir)/src/libfontconfig.la /usr/lib/libz.a",
        )
        mk.write_text(text)

    mk = self.cwd / "build/test/Makefile"
    if mk.exists():
        text = mk.read_text()
        text = text.replace(
            "${top_builddir}/src/libfontconfig.la",
            "${top_builddir}/src/libfontconfig.la /usr/lib/libz.a",
        )
        text = text.replace(
            "$(top_builddir)/src/libfontconfig.la",
            "$(top_builddir)/src/libfontconfig.la /usr/lib/libz.a",
        )
        mk.write_text(text)



@subpackage("fontconfig-devel")
def _(self):
    return self.default_devel()


def post_install(self):
    self.install_license("COPYING")
