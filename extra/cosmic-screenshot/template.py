pkgname = "cosmic-screenshot"
pkgver = "1.11.0"
pkgrel = 0
archs = ["x86_64"]
hostmakedepends = ["cargo-bootstrap", "git", "pkgconf", "rust"]
makedepends = ["libxkbcommon-devel", "wayland-devel"]
depends = ["cosmic-icons", "xdg-desktop-portal-cosmic"]
pkgdesc = "Screenshot utility for the COSMIC desktop environment"
license = "GPL-3.0-only"
url = "https://github.com/pop-os/cosmic-screenshot"
source = f"https://github.com/pop-os/cosmic-screenshot/archive/refs/tags/epoch-{pkgver}.tar.gz"
sha256 = "0bf658bda69ce67113d58d1ad5d32126218095194cc51f69c27b8d6399962af7"
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
    appid = "com.system76.CosmicScreenshot"

    self.install_bin("target/release/cosmic-screenshot")
    self.install_file(f"resources/{appid}.desktop", "usr/share/applications")

    icons = self.cwd / "resources/icons/hicolor"
    for path in icons.rglob("*"):
        if path.is_file():
            rel = path.relative_to(icons)
            self.install_file(
                f"resources/icons/hicolor/{rel}",
                f"usr/share/icons/hicolor/{rel.parent}",
            )

    self.install_license("LICENSE")
