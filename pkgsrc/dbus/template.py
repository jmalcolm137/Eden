pkgname = "dbus"
pkgver = "1.16.4"
pkgrel = 1
build_style = "meson"
configure_args = [
    "-Dapparmor=disabled",
    "-Dasserts=false",
    "-Ddbus_user=dbus",
    "-Ddoxygen_docs=disabled",
    "-Dducktype_docs=disabled",
    "-Depoll=enabled",
    "-Dinotify=enabled",
    "-Dlibaudit=disabled",
    "-Dselinux=disabled",
    "-Dsystemd=disabled",
    "-Dtools=true",
    "-Dtraditional_activation=true",
    "-Duser_session=false",
    "-Dxml_docs=disabled",
]
meson_impl = "meson"
hostmakedepends = ["meson-real", "pkgconf", "python", "samurai"]
makedepends = ["libexpat-devel", "linux-headers"]
pkgdesc = "Message bus system"
license = "GPL-2.0-or-later"
url = "https://dbus.freedesktop.org"
source = "https://dbus.freedesktop.org/releases/dbus/dbus-1.16.4.tar.xz"
sha256 = "d08b05526c2cb7966a5fb79210d6112b1aca3d135f315c1b302e14b4b0297dac"
# tests need a running message bus
options = ["etcfiles", "!check"]


@subpackage("dbus-libs")
def _(self):
    return self.default_libs()


@subpackage("dbus-devel")
def _(self):
    return self.default_devel(extra=["usr/lib/dbus-1.0/include"])


def post_install(self):
    self.install_license("COPYING")
