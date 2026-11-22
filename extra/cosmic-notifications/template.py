pkgname = "cosmic-notifications"
pkgver = "1.11.0"
pkgrel = 0
archs = ["x86_64"]
hostmakedepends = ['cargo-bootstrap', 'git', 'pkgconf', 'rust']
makedepends = ['libxkbcommon-devel', 'wayland-devel']
pkgdesc = "Notification daemon for the COSMIC desktop environment"
license = "GPL-3.0-only"
url = "https://github.com/pop-os/cosmic-notifications"
source = f"https://github.com/pop-os/cosmic-notifications/archive/refs/tags/epoch-{pkgver}.tar.gz"
sha256 = "1874d0b5d67a0c6f1c1415f36a094faaac9c82f3ddf4eeb5061c516d778598c8"
# the test suite needs a running compositor
options = ["!check"]

_cargo_env = {
    "CARGO_HOME": "/cbuild_cache/cargo",
    "CARGO_NET_OFFLINE": "true",
}


def prepare(self):
    self.do(
        "cargo",
        "fetch",
        "--locked",
        env={"CARGO_HOME": "/cbuild_cache/cargo"},
        allow_network=True,
    )


def build(self):
    self.do("cargo", "build", "--release", "--locked", "--no-default-features", env=_cargo_env)


def install(self):
    self.install_bin("target/release/cosmic-notifications")
    self.install_license("LICENSE.md")
