pkgname = "cosmic-comp"
pkgver = "1.11.0"
pkgrel = 0
archs = ["x86_64"]
hostmakedepends = ["cargo-bootstrap", "git", "pkgconf", "rust"]
makedepends = [
    "fontconfig-devel",
    "libdisplay-info-devel",
    "libdrm-devel",
    "libinput-devel",
    "libseat-devel",
    "libxcb-devel",
    "libxkbcommon-devel",
    "mesa-devel",
    "pixman-devel",
    "wayland-devel",
]
pkgdesc = "COSMIC Wayland compositor"
license = "GPL-3.0-only"
url = "https://github.com/pop-os/cosmic-comp"
source = f"https://github.com/pop-os/cosmic-comp/archive/refs/tags/epoch-{pkgver}.tar.gz"
sha256 = "c07778440f25e909358a37f293ddf403a28a153b02eedb30b61b846a7142ba60"
# the test suite needs a running compositor and display
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
    # systemd/logind are replaced by perp and seatd on Eden.  libseat handles
    # seat and VT management, so the systemd feature is not needed.
    self.do(
        "cargo",
        "build",
        "--release",
        "--locked",
        "--no-default-features",
        env=_cargo_env,
    )


def install(self):
    self.install_bin("target/release/cosmic-comp")

    self.install_file(
        "data/keybindings.ron",
        "usr/share/cosmic/com.system76.CosmicSettings.Shortcuts/v1",
        name="defaults",
    )
    self.install_file(
        "data/tiling-exceptions.ron",
        "usr/share/cosmic/com.system76.CosmicSettings.WindowRules/v1",
        name="tiling_exception_defaults",
    )

    self.install_license("LICENSE")
