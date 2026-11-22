pkgname = "cosmic-bg"
pkgver = "1.11.0"
pkgrel = 0
archs = ["x86_64"]
hostmakedepends = ['cargo-bootstrap', 'git', 'pkgconf', 'rust']
makedepends = ['libxkbcommon-devel']
pkgdesc = "Background service for the COSMIC desktop environment"
license = "MPL-2.0"
url = "https://github.com/pop-os/cosmic-bg"
source = f"https://github.com/pop-os/cosmic-bg/archive/refs/tags/epoch-{pkgver}.tar.gz"
sha256 = "00e0874b82877378be9cb305139e626f3cd5ef01ad7a1a517de826086adc2652"
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
    # AVIF support needs libdav1d; PNG/JPEG wallpapers do not.
    self.do(
        "cargo",
        "build",
        "--release",
        "--locked",
        "--no-default-features",
        env=_cargo_env,
    )


def install(self):
    self.install_bin("target/release/cosmic-bg")

    data = self.cwd / "data/v1"
    for path in data.rglob("*"):
        if path.is_file():
            rel = path.relative_to(data)
            self.install_file(
                f"data/v1/{rel}",
                f"usr/share/cosmic/com.system76.CosmicBackground/v1/{rel.parent}",
            )

    self.install_license("LICENSE.md")
