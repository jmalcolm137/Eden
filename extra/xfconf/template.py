pkgname = "xfconf"
pkgver = "4.21.2"
pkgrel = 1
build_style = "meson"
configure_args = [
    "-Dintrospection=false",
    "-Dvala=disabled",
    "-Dgtk-doc=false",
    "-Dtests=false",
    "-Dgsettings-backend=true",
]
hostmakedepends = [
    "gettext",
    "glib-devel",
    "muon",
    "pkgconf",
    "python",
    "samurai",
    "xfce4-dev-tools",
]
makedepends = [
    "glib-devel",
    "libxfce4util-devel",
]
pkgdesc = "Xfce configuration system"
license = "GPL-2.0-only AND LGPL-2.0-or-later"
url = "https://docs.xfce.org/xfce/xfconf/start"
source = f"https://archive.xfce.org/src/xfce/xfconf/4.21/xfconf-4.21.2.tar.xz"
sha256 = "99aa4366e909ba7b9f746aba48b610b9e9d2933aeb283c7fa5f37a7c3dc7a3a6"
# upstream tests need a display and a running session bus
options = ["!check", "etcfiles"]


def post_install(self):
    self.uninstall("usr/lib/systemd/user", missing_ok=True)


@subpackage("xfconf-devel")
def _(self):
    return self.default_devel()


def post_patch(self):
    # muon requires the annotations list to be a list of lists
    mf = self.cwd / "common/meson.build"
    text = mf.read_text()
    old = "    annotations: ['@0@.Xfconf'.format(xfconf_service_name_prefix), 'org.gtk.GDBus.C.Name', 'Exported'],"
    new = "    annotations: [['@0@.Xfconf'.format(xfconf_service_name_prefix), 'org.gtk.GDBus.C.Name', 'Exported']],"
    if old not in text:
        self.error("unexpected gdbus annotations in meson.build")
    mf.write_text(text.replace(old, new))
