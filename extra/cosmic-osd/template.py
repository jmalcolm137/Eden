pkgname = "cosmic-osd"
pkgver = "1.11.0"
pkgrel = 0
archs = ["x86_64"]
hostmakedepends = ["cargo-bootstrap", "git", "pkgconf", "rust"]
makedepends = [
    "clang-libs",
    "libinput-devel",
    "libpulse-devel",
    "libxkbcommon-devel",
    "llvm-devel",
    "pipewire-devel",
    "udev-devel",
    "wayland-devel",
]
pkgdesc = "On-screen display for the COSMIC desktop environment"
license = "GPL-3.0-or-later"
url = "https://github.com/pop-os/cosmic-osd"
source = f"https://github.com/pop-os/cosmic-osd/archive/refs/tags/epoch-{pkgver}.tar.gz"
sha256 = "98f049d10e9746ae9751d10d556eff73b7270d7d99861445ab9171bd140ba416"
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
    self.install_bin("target/release/cosmic-osd")
    self.install_license("LICENSE")
