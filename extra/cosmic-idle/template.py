pkgname = "cosmic-idle"
pkgver = "1.11.0"
pkgrel = 0
archs = ["x86_64"]
hostmakedepends = ['cargo-bootstrap', 'git', 'pkgconf', 'rust']
makedepends = ['libxkbcommon-devel', 'wayland-devel']
pkgdesc = "Idle daemon for the COSMIC desktop environment"
license = "GPL-3.0-only"
url = "https://github.com/pop-os/cosmic-idle"
source = f"https://github.com/pop-os/cosmic-idle/archive/refs/tags/epoch-{pkgver}.tar.gz"
sha256 = "683290f2a67a63fd553f654a34756cbfdcc41b2d2141b79850c58c16643dc63a"
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
    self.do("cargo", "build", "--release", "--locked", env=_cargo_env)


def install(self):
    self.install_bin("target/release/cosmic-idle")
    self.install_license("LICENSE")
