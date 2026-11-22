pkgname = "cosmic-workspaces"
pkgver = "1.11.0"
pkgrel = 0
archs = ["x86_64"]
hostmakedepends = ['cargo-bootstrap', 'git', 'pkgconf', 'rust']
makedepends = ['libinput-devel', 'libxkbcommon-devel', 'mesa-devel', 'wayland-devel', 'wayland-protocols']
pkgdesc = "Workspace overview for the COSMIC desktop environment"
license = "GPL-3.0-only"
url = "https://github.com/pop-os/cosmic-workspaces-epoch"
source = f"https://github.com/pop-os/cosmic-workspaces-epoch/archive/refs/tags/epoch-{pkgver}.tar.gz"
sha256 = "4dad3cd1fffe5b377c84948598c666493e5a053e6e1105a958f20a73bea92eab"
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
    appid = "com.system76.CosmicWorkspaces"

    self.install_bin("target/release/cosmic-workspaces")
    self.install_file(f"data/{appid}.desktop", "usr/share/applications")
    self.install_file(
        f"data/{appid}.svg", "usr/share/icons/hicolor/scalable/apps"
    )
    self.install_license("LICENSE")
