pkgname = "cosmic-files"
pkgver = "1.11.0"
pkgrel = 0
archs = ["x86_64"]
hostmakedepends = ["cargo-bootstrap", "git", "pkgconf", "rust"]
makedepends = ['glib-devel', 'libxkbcommon-devel', 'wayland-devel']
pkgdesc = "Cosmic Files for the COSMIC desktop environment"
license = "GPL-3.0-only"
url = "https://github.com/pop-os/cosmic-files"
source = f"https://github.com/pop-os/cosmic-files/archive/refs/tags/epoch-{pkgver}.tar.gz"
sha256 = "ceeea09a6e249192a8e439d416f20391e923cb75c09922297ff9e6b9926e8eb7"
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
    self.do("cargo", "build", "--release", "--locked", "--workspace", env=_cargo_env)


def install(self):
    appid = "com.system76.CosmicFiles"

    self.install_bin("target/release/cosmic-files")
    self.install_bin("target/release/cosmic-files-thumbnailer")
    self.install_bin("target/release/cosmic-files-applet")

    desktop = self.cwd / "target/xdgen" / f"{appid}.desktop"
    if not desktop.is_file():
        desktop = self.cwd / "res" / f"{appid}.desktop"
    self.install_file(desktop.relative_to(self.cwd), "usr/share/applications")

    metainfo = self.cwd / "target/xdgen" / f"{appid}.metainfo.xml"
    if not metainfo.is_file():
        metainfo = self.cwd / "res" / f"{appid}.metainfo.xml"
    self.install_file(metainfo.relative_to(self.cwd), "usr/share/metainfo")

    self.install_file("res/com.system76.CosmicFiles.thumbnailer", "usr/share/thumbnailers")

    icons = self.cwd / "res/icons/hicolor"
    for path in icons.rglob("*"):
        if path.is_file():
            rel = path.relative_to(icons)
            self.install_file(
                f"res/icons/hicolor/{rel}",
                f"usr/share/icons/hicolor/{rel.parent}",
            )

    self.install_license("LICENSE")
