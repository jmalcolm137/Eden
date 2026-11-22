pkgname = "cosmic-randr"
pkgver = "1.11.0"
pkgrel = 0
archs = ["x86_64"]
hostmakedepends = ['cargo-bootstrap', 'git', 'pkgconf', 'rust']
makedepends = []
pkgdesc = "Display configuration library and CLI for COSMIC"
license = "MPL-2.0"
url = "https://github.com/pop-os/cosmic-randr"
source = f"https://github.com/pop-os/cosmic-randr/archive/refs/tags/epoch-{pkgver}.tar.gz"
sha256 = "cd04841b780ad13d407a0a3740f827b3fc214dfc198b114d6a83524c2a0ca96e"
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
    self.install_bin("target/release/cosmic-randr")
    self.install_license("LICENSE")
