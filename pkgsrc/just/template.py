pkgname = "just"
pkgver = "1.59.0"
pkgrel = 0
archs = ["x86_64"]
hostmakedepends = ["cargo-bootstrap", "rust"]
pkgdesc = "Just a command runner"
license = "CC0-1.0"
url = "https://github.com/casey/just"
source = f"https://github.com/casey/just/archive/{pkgver}/just-{pkgver}.tar.gz"
sha256 = "20f876880851f1cc67fc7eb7589c7f7ccaa7612d827feac75797cf4a6ed729aa"
# the upstream test suite needs a fully configured shell environment
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
    self.install_bin("target/release/just")

    self.do("sh", "-c", "./target/release/just --man > just.1")
    self.install_man("just.1")

    for shell in ["bash", "fish", "zsh"]:
        self.install_completion(f"completions/just.{shell}", shell)

    self.install_license("LICENSE")
