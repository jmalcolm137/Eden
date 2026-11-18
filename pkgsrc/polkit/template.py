pkgname = "polkit"
pkgver = "128"
pkgrel = 1
build_style = "meson"
configure_args = [
    "-Dauthfw=shadow",
    "-Dexamples=false",
    "-Dgettext=false",
    "-Dgtk_doc=false",
    "-Dintrospection=false",
    "-Dlibs-only=true",
    "-Dman=false",
    "-Dsession_tracking=ConsoleKit",
    "-Dtests=false",
 ]
meson_impl = "meson"
hostmakedepends = ["gettext", "meson-real", "pkgconf", "python", "samurai"]
makedepends = ["dbus-devel", "glib-devel"]
pkgdesc = "Authorization manager"
license = "LGPL-2.0-or-later"
url = "https://github.com/polkit-org/polkit"
source = "https://github.com/polkit-org/polkit/archive/refs/tags/128.tar.gz"
sha256 = "6edb06bf1448e49e428f9597a97af6a05d62146dd0b58f86eeaebcee3f5ecfaa"
# only the client libraries are needed by the desktop build
options = ["!check"]


@subpackage("polkit-libs")
def _(self):
    return self.default_libs()


@subpackage("polkit-devel")
def _(self):
    return self.default_devel()


def post_install(self):
    self.install_license("COPYING")
