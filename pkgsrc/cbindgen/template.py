pkgname = "cbindgen"
pkgver = "0.29.4"
pkgrel = 0
archs = ["x86_64"]
hostmakedepends = ["cargo-bootstrap", "rust"]
pkgdesc = "Tool to generate C bindings from Rust code"
license = "MPL-2.0"
url = "https://github.com/mozilla/cbindgen"
source = f"https://github.com/mozilla/cbindgen/archive/refs/tags/{pkgver}.tar.gz"
sha256 = "9b5757e915cf8be523d3aca282b9b5651bafa112e14bf1ba488562ba282807d6"
# the test suite needs a full Rust workspace
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
    self.install_bin("target/release/cbindgen")
    self.install_license("LICENSE")
