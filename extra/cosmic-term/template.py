pkgname = "cosmic-term"
pkgver = "1.11.0"
pkgrel = 0
archs = ["x86_64"]
hostmakedepends = ["cargo-bootstrap", "git", "pkgconf", "rust"]
makedepends = ['libxkbcommon-devel', 'wayland-devel']
pkgdesc = "Cosmic Term for the COSMIC desktop environment"
license = "GPL-3.0-only"
url = "https://github.com/pop-os/cosmic-term"
source = f"https://github.com/pop-os/cosmic-term/archive/refs/tags/epoch-{pkgver}.tar.gz"
sha256 = "455cdc42e8f4a5a00a033a38f65341bf1b1af621cc7d01a78da0ee2f9177a09c"
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
    appid = "com.system76.CosmicTerm"

    self.install_bin("target/release/cosmic-term")

    desktop = self.cwd / "target/xdgen" / f"{appid}.desktop"
    if not desktop.is_file():
        desktop = self.cwd / "res" / f"{appid}.desktop"
    self.install_file(desktop.relative_to(self.cwd), "usr/share/applications")

    metainfo = self.cwd / "target/xdgen" / f"{appid}.metainfo.xml"
    if not metainfo.is_file():
        metainfo = self.cwd / "res" / f"{appid}.metainfo.xml"
    self.install_file(metainfo.relative_to(self.cwd), "usr/share/metainfo")

    icons = self.cwd / "res/icons/hicolor"
    for path in icons.rglob("*"):
        if path.is_file():
            rel = path.relative_to(icons)
            self.install_file(
                f"res/icons/hicolor/{rel}",
                f"usr/share/icons/hicolor/{rel.parent}",
            )

    self.install_license("LICENSE")
