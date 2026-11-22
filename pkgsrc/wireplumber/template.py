pkgname = "wireplumber"
pkgver = "0.5.19"
pkgrel = 0
archs = ["x86_64"]
build_style = "meson"
configure_args = [
    "-Ddbus-tests=false",
    "-Ddefault_library=shared",
    "-Ddoc=disabled",
    "-Delogind=disabled",
    "-Dintrospection=disabled",
    "-Dsystemd=disabled",
    "-Dsystemd-system-service=false",
    "-Dsystemd-user-service=false",
    "-Dtests=false",
]
hostmakedepends = ["meson-real", "pkgconf", "samurai"]
makedepends = ["glib-devel", "pipewire-devel"]
depends = ["pipewire"]
pkgdesc = "Session and policy manager for PipeWire"
license = "MIT"
url = "https://pipewire.org"
source = f"https://github.com/PipeWire/wireplumber/archive/refs/tags/{pkgver}.tar.gz"
sha256 = "f9454eae3a5a6ca903c05ead2a7e47d7d3957fb0ffac3ebb11d92842603ae80f"
# the test suite needs a running PipeWire session and D-Bus
options = ["!check"]


def prepare(self):
    # The bundled Lua is a meson wrap-file; fetch it while the network is up.
    self.do("meson", "subprojects", "download", allow_network=True)


def post_install(self):
    self.rm(self.destdir / "usr/lib/systemd", recursive=True, force=True)
    for path in (self.destdir / "usr/lib").glob("*.a"):
        path.unlink()
    self.install_file(
        self.files_path / "perp/wireplumber/rc.main",
        "usr/share/wireplumber/perp/wireplumber",
        mode=0o755,
    )
    (self.destdir / "usr/share/wireplumber/perp/wireplumber").chmod(0o1755)
    self.install_license("LICENSE")
