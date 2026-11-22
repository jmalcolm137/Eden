pkgname = "cosmic-panel"
pkgver = "1.11.0"
pkgrel = 0
archs = ["x86_64"]
hostmakedepends = ["cargo-bootstrap", "git", "pkgconf", "rust"]
makedepends = ["libxkbcommon-devel", "wayland-devel", "wayland-protocols"]
pkgdesc = "Panel for the COSMIC desktop environment"
license = "GPL-3.0-only"
url = "https://github.com/pop-os/cosmic-panel"
source = f"https://github.com/pop-os/cosmic-panel/archive/refs/tags/epoch-{pkgver}.tar.gz"
sha256 = "ef0de256580e1f1600c5a662179862976ba0b8475b45e99e9eb2713bed8e1007"
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
    self.install_bin("target/release/cosmic-panel")

    schema = self.cwd / "data/default_schema"
    for path in schema.rglob("*"):
        if path.is_file():
            rel = path.relative_to(schema)
            self.install_file(
                f"data/default_schema/{rel}", f"usr/share/cosmic/{rel.parent}"
            )

    self.install_license("LICENSE.md")
