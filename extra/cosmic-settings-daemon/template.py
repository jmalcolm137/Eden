pkgname = "cosmic-settings-daemon"
pkgver = "1.11.0"
pkgrel = 0
archs = ["x86_64"]
hostmakedepends = ["cargo-bootstrap", "git", "pkgconf", "rust"]
makedepends = [
    "clang-libs",
    "libinput-devel",
    "libxkbcommon-devel",
    "llvm-devel",
    "openssl",
    "pipewire-devel",
]
pkgdesc = "Settings daemon for the COSMIC desktop environment"
license = "GPL-3.0-only"
url = "https://github.com/pop-os/cosmic-settings-daemon"
source = f"https://github.com/pop-os/cosmic-settings-daemon/archive/refs/tags/epoch-{pkgver}.tar.gz"
sha256 = "1cc494c028a59a0356547c834421495da326622f837221726c15fceb14f3f9f0"
# the test suite needs a running session and audio devices
options = ["!check"]

_cargo_env = {
    "CARGO_HOME": "/cbuild_cache/cargo",
    "CARGO_NET_OFFLINE": "true",
    "LIBCLANG_PATH": "/usr/lib",
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
    self.install_bin("target/release/cosmic-settings-daemon")

    self.install_file(
        "data/system_actions.ron",
        "usr/share/cosmic/com.system76.CosmicSettings.Shortcuts/v1",
        name="system_actions",
    )
    self.install_file(
        "data/polkit-1/rules.d/cosmic-settings-daemon.rules",
        "usr/share/polkit-1/rules.d",
    )

    self.install_license("LICENSE")
