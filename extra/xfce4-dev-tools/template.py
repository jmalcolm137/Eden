pkgname = "xfce4-dev-tools"
pkgver = "4.21.2"
pkgrel = 0
build_style = "gnu_configure"
configure_gen = []
make_build_args = ["SUBDIRS=scripts xdt-csource m4macros"]
make_install_args = [*make_build_args]
hostmakedepends = ["libxslt-progs", "meson", "pkgconf"]
makedepends = ["glib-devel"]
depends = ["python"]
pkgdesc = "Development tools for building Xfce"
license = "GPL-2.0-or-later"
url = "https://docs.xfce.org/xfce/xfce4-dev-tools/start"
source = f"https://archive.xfce.org/src/xfce/xfce4-dev-tools/4.21/xfce4-dev-tools-{pkgver}.tar.bz2"
sha256 = "a43f726a082b589186d9e6ed076101d41249d1e22bbe61448037550190d7f75a"
# upstream tests need a display and a running session bus
options = ["!check"]


def pre_configure(self):
    # this tree provides meson as muon; the configure check only looks for a
    # binary called meson, and xdt-autogen then records the detected path
    cf = self.cwd / "configure"
    text = cf.read_text()
    old = "for ac_prog in meson\n"

    if old not in text:
        self.error("unexpected meson check in configure")

    cf.write_text(text.replace(old, "for ac_prog in meson muon\n"))
