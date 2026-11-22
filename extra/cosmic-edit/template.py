pkgname = "cosmic-edit"
pkgver = "1.11.0"
pkgrel = 0
archs = ["x86_64"]
hostmakedepends = ["cargo-bootstrap", "git", "pkgconf", "rust"]
makedepends = [
    "glib-devel",
    "libxkbcommon-devel",
    "oniguruma-devel",
    "wayland-devel",
]
pkgdesc = "Text editor for the COSMIC desktop environment"
license = "GPL-3.0-only"
url = "https://github.com/pop-os/cosmic-edit"
source = f"https://github.com/pop-os/cosmic-edit/archive/refs/tags/epoch-{pkgver}.tar.gz"
sha256 = "aff1a305a4e7182ae1c360ceac43eff60ba32dc388f872f3ec04624677a6a290"
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
    appid = "com.system76.CosmicEdit"

    self.install_bin("target/release/cosmic-edit")
    self.install_file(f"target/xdgen/{appid}.desktop", "usr/share/applications")
    self.install_file(
        f"target/xdgen/{appid}.metainfo.xml", "usr/share/metainfo"
    )

    icons = self.cwd / "res/icons/hicolor"
    for path in icons.rglob("*"):
        if path.is_file():
            rel = path.relative_to(icons)
            self.install_file(
                f"res/icons/hicolor/{rel}",
                f"usr/share/icons/hicolor/{rel.parent}",
            )

    self.install_license("LICENSE")
