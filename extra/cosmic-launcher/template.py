pkgname = "cosmic-launcher"
pkgver = "1.11.0"
pkgrel = 0
archs = ["x86_64"]
hostmakedepends = ['cargo-bootstrap', 'git', 'pkgconf', 'rust']
makedepends = ['libxkbcommon-devel', 'wayland-devel', 'wayland-protocols']
depends = ['pop-launcher']
pkgdesc = "Application launcher for the COSMIC desktop environment"
license = "GPL-3.0-only"
url = "https://github.com/pop-os/cosmic-launcher"
source = f"https://github.com/pop-os/cosmic-launcher/archive/refs/tags/epoch-{pkgver}.tar.gz"
sha256 = "82a510d7d472c68cdd1137363704c1f6a91b37de4f48e5a1f844242de79f941d"
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
    appid = "com.system76.CosmicLauncher"

    self.install_bin("target/release/cosmic-launcher")
    self.install_file(
        f"target/xdgen/{appid}.desktop", "usr/share/applications"
    )
    self.install_file(f"target/xdgen/{appid}.metainfo.xml", "usr/share/appdata")
    self.install_file(
        f"data/icons/{appid}.svg",
        "usr/share/icons/hicolor/scalable/apps",
    )
    self.install_license("LICENSE.md")
