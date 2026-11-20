pkgname = "xorgproto"
pkgver = "2024.1"
pkgrel = 0
build_style = "gnu_configure"
configure_args = ["--enable-legacy"]
configure_env = {"M4": "/usr/bin/gm4"}
hostmakedepends = ["automake", "libtool", "pkgconf", "xorg-util-macros"]
pkgdesc = "Combined X.Org X11 protocol headers"
license = "MIT"
url = "https://xorg.freedesktop.org"
source = f"https://xorg.freedesktop.org/releases/individual/proto/xorgproto-{pkgver}.tar.gz"
sha256 = "4f6b9b4faf91e5df8265b71843a91fc73dc895be6210c84117a996545df296ce"
# upstream test suites need a full X session
options = ["!check", "!scanrundeps"]


def post_install(self):
    for f in self.cwd.glob("COPYING-*"):
        self.install_license(f)
