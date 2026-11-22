pkgname = "cosmic-app-library"
pkgver = "1.11.0"
pkgrel = 0
archs = ["x86_64"]
hostmakedepends = ['cargo-bootstrap', 'git', 'pkgconf', 'rust']
makedepends = ['libxkbcommon-devel']
pkgdesc = "Application library for the COSMIC desktop environment"
license = "GPL-3.0-only"
url = "https://github.com/pop-os/cosmic-applibrary"
source = f"https://github.com/pop-os/cosmic-applibrary/archive/refs/tags/epoch-{pkgver}.tar.gz"
sha256 = "9ce3f012af1f885b0a99c589e77803c8d7fb76cba7a7202030cae19f1ac2dd55"
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
    appid = "com.system76.CosmicAppLibrary"

    self.install_bin("target/release/cosmic-app-library")
    self.install_file(
        f"target/xdgen/{appid}.desktop", "usr/share/applications"
    )
    self.install_file(f"target/xdgen/{appid}.metainfo.xml", "usr/share/appdata")
    self.install_file(
        f"data/icons/{appid}.svg",
        "usr/share/icons/hicolor/scalable/apps",
    )
    self.install_license("LICENSE.md")
