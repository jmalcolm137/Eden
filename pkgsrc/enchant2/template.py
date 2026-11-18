pkgname = "enchant2"
pkgver = "2.8.21"
pkgrel = 1
build_style = "gnu_configure"
configure_args = [
    "--disable-static",
    "--disable-gcc-warnings",
]
configure_gen = []
hostmakedepends = ["libtool", "pkgconf"]
makedepends = ["glib-devel"]
pkgdesc = "Spellchecking library"
license = "LGPL-2.1-or-later"
url = "https://rrthomas.github.io/enchant"
source = f"https://github.com/rrthomas/enchant/releases/download/v{pkgver}/enchant-{pkgver}.tar.gz"
sha256 = "dd2a762697c463148a8f59867089a5ebf2dd1449d869f93764b76c12bcf8acc0"
# tests need installed dictionaries
options = ["!check"]


@subpackage("enchant2-devel")
def _(self):
    return self.default_devel()


@subpackage("enchant2-progs")
def _(self):
    return self.default_progs()


def post_install(self):
    self.install_license("COPYING.LIB")


def post_patch(self):
    # groff is not available; the html man pages are not needed
    for p in self.cwd.glob("**/Makefile.*"):
        if not p.is_file():
            continue
        text = p.read_text()
        if "groff -mandoc -Thtml" not in text:
            continue
        p.write_text(text.replace("groff -mandoc -Thtml $< > $@", ": > $@"))
    # ensure the generated makefiles are not regenerated
    for p in self.cwd.glob("**/Makefile.in"):
        p.touch()


def pre_install(self):
    # no providers are built, so the module dir does not exist yet
    (self.destdir / "usr/lib/enchant-2").mkdir(parents=True, exist_ok=True)
