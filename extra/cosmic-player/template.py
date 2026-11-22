pkgname = "cosmic-player"
pkgver = "1.11.0"
pkgrel = 0
archs = ["x86_64"]
hostmakedepends = ["cargo-bootstrap", "git", "pkgconf", "rust"]
makedepends = ['glib-devel', 'gst-plugins-base-devel', 'gstreamer-devel', 'libxkbcommon-devel', 'wayland-devel']
pkgdesc = "Cosmic Player for the COSMIC desktop environment"
license = "GPL-3.0-only"
url = "https://github.com/pop-os/cosmic-player"
source = f"https://github.com/pop-os/cosmic-player/archive/refs/tags/epoch-{pkgver}.tar.gz"
sha256 = "25a9edfdaaa0b6b46a03315d1cae0b7590e2827e4172801688db4b7a2ff96f1f"
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
    appid = "com.system76.CosmicPlayer"

    self.install_bin("target/release/cosmic-player")

    desktop = self.cwd / "target/xdgen" / f"{appid}.desktop"
    if not desktop.is_file():
        desktop = self.cwd / "res" / f"{appid}.desktop"
    self.install_file(desktop.relative_to(self.cwd), "usr/share/applications")

    metainfo = self.cwd / "target/xdgen" / f"{appid}.metainfo.xml"
    if not metainfo.is_file():
        metainfo = self.cwd / "res" / f"{appid}.metainfo.xml"
    self.install_file(metainfo.relative_to(self.cwd), "usr/share/metainfo")

    self.install_file("res/com.system76.CosmicPlayer.thumbnailer", "usr/share/thumbnailers")

    icons = self.cwd / "res/icons/hicolor"
    for path in icons.rglob("*"):
        if path.is_file():
            rel = path.relative_to(icons)
            self.install_file(
                f"res/icons/hicolor/{rel}",
                f"usr/share/icons/hicolor/{rel.parent}",
            )

    self.install_license("LICENSE")
