pkgname = "cosmic-settings"
pkgver = "1.11.0"
pkgrel = 0
archs = ["x86_64"]
hostmakedepends = ["cargo-bootstrap", "git", "pkgconf", "rust"]
makedepends = [
    "dbus-devel",
    "fontconfig-devel",
    "iso-codes",
    "libinput-devel",
    "libxkbcommon-devel",
    "udev-devel",
    "wayland-devel",
]
depends = ["cosmic-icons", "polkit"]
pkgdesc = "Settings application for the COSMIC desktop environment"
license = "GPL-3.0-only"
url = "https://github.com/pop-os/cosmic-settings"
source = f"https://github.com/pop-os/cosmic-settings/archive/refs/tags/epoch-{pkgver}.tar.gz"
sha256 = "213459e770dc899da7f9d47557b7d3e4e27e1debb8d7af590995bd0f63da0a5e"
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
    self.do(
        "cargo",
        "build",
        "--release",
        "--locked",
        "--no-default-features",
        "--features",
        "a11y,linux,single-instance,wgpu,perp",
        env=_cargo_env,
    )


def install(self):
    self.install_bin("target/release/cosmic-settings")

    self.install_file(
        "resources/com.system76.CosmicSettings.metainfo.xml", "usr/share/metainfo"
    )
    self.install_file(
        "resources/polkit-1/rules.d/cosmic-settings.rules",
        "usr/share/polkit-1/rules.d",
    )
    self.install_file(
        "resources/polkit-1/actions/com.system76.CosmicSettings.Users.policy",
        "usr/share/polkit-1/actions",
    )

    for path in (self.cwd / "target/xdgen").rglob("*"):
        if path.is_file():
            rel = path.relative_to(self.cwd / "target/xdgen")
            self.install_file(f"target/xdgen/{rel}", f"usr/share/applications/{rel.parent}")

    schema = self.cwd / "resources/default_schema"
    for path in schema.rglob("*"):
        if path.is_file():
            rel = path.relative_to(schema)
            self.install_file(
                f"resources/default_schema/{rel}", f"usr/share/cosmic/{rel.parent}"
            )

    icons = self.cwd / "resources/icons"
    for path in icons.rglob("*"):
        if path.is_file():
            rel = path.relative_to(icons)
            self.install_file(
                f"resources/icons/{rel}", f"usr/share/icons/hicolor/{rel.parent}"
            )

    self.install_license("LICENSE.md")
