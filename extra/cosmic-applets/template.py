pkgname = "cosmic-applets"
pkgver = "1.11.0"
pkgrel = 0
archs = ["x86_64"]
hostmakedepends = ["cargo-bootstrap", "git", "pkgconf", "rust"]
makedepends = ["dbus-devel", "libinput-devel", "libxkbcommon-devel", "wayland-devel"]
pkgdesc = "Panel applets for the COSMIC desktop environment"
license = "GPL-3.0-only"
url = "https://github.com/pop-os/cosmic-applets"
source = f"https://github.com/pop-os/cosmic-applets/archive/refs/tags/epoch-{pkgver}.tar.gz"
sha256 = "d2ad09b72a2dcba2a17f12e557f0e21dc60171eefa54390e4b67bb058f9180e2"
# the test suite needs a running compositor
options = ["!check"]

_cargo_env = {
    "CARGO_HOME": "/cbuild_cache/cargo",
    "CARGO_NET_OFFLINE": "true",
}

_applets = [
    ("com.system76.CosmicAppList", "cosmic-app-list"),
    ("com.system76.CosmicAppletA11y", "cosmic-applet-a11y"),
    ("com.system76.CosmicAppletAudio", "cosmic-applet-audio"),
    ("com.system76.CosmicAppletInputSources", "cosmic-applet-input-sources"),
    ("com.system76.CosmicAppletBattery", "cosmic-applet-battery"),
    ("com.system76.CosmicAppletBluetooth", "cosmic-applet-bluetooth"),
    ("com.system76.CosmicAppletMinimize", "cosmic-applet-minimize"),
    ("com.system76.CosmicAppletNetwork", "cosmic-applet-network"),
    ("com.system76.CosmicAppletNotifications", "cosmic-applet-notifications"),
    ("com.system76.CosmicAppletOsk", "cosmic-applet-osk"),
    ("com.system76.CosmicAppletPower", "cosmic-applet-power"),
    ("com.system76.CosmicAppletStatusArea", "cosmic-applet-status-area"),
    ("com.system76.CosmicAppletTiling", "cosmic-applet-tiling"),
    ("com.system76.CosmicAppletTime", "cosmic-applet-time"),
    ("com.system76.CosmicAppletWorkspaces", "cosmic-applet-workspaces"),
]

_buttons = [
    ("com.system76.CosmicPanelAppButton", "cosmic-panel-app-button"),
    ("com.system76.CosmicPanelLauncherButton", "cosmic-panel-launcher-button"),
    ("com.system76.CosmicPanelWorkspacesButton", "cosmic-panel-workspaces-button"),
]


def prepare(self):
    self.do(
        "cargo",
        "fetch",
        "--locked",
        env={"CARGO_HOME": "/cbuild_cache/cargo"},
        allow_network=True,
    )


def post_patch(self):
    # The status notifier is D-Bus activated; the systemd user unit that the
    # upstream install rule also writes is not used here.
    p = (
        self.cwd
        / "cosmic-applet-status-area/data/dbus-1/com.system76.CosmicStatusNotifierWatcher.service.in"
    )
    text = p.read_text().replace("@bindir@", "/usr/bin")
    (p.parent / "com.system76.CosmicStatusNotifierWatcher.service").write_text(text)


def build(self):
    self.do("cargo", "build", "--release", "--locked", env=_cargo_env)


def install(self):
    self.install_bin("target/release/cosmic-applets")
    self.install_link("usr/bin/cosmic-panel-button", "cosmic-applets")

    for appid, name in _applets + _buttons:
        icons = self.cwd / name / "data/icons"
        if icons.is_dir():
            for path in icons.rglob("*"):
                if path.is_file():
                    rel = path.relative_to(icons)
                    self.install_file(
                        f"{name}/data/icons/{rel}", f"usr/share/icons/hicolor/{rel.parent}"
                    )

        self.install_file(
            f"target/xdgen/{appid}.desktop", "usr/share/applications"
        )

        if (appid, name) in _applets:
            self.install_link(f"usr/bin/{name}", "cosmic-applets")

    schema = self.cwd / "cosmic-app-list/data/default_schema"
    for path in schema.rglob("*"):
        if path.is_file():
            rel = path.relative_to(schema)
            self.install_file(
                f"cosmic-app-list/data/default_schema/{rel}",
                f"usr/share/cosmic/{rel.parent}",
            )

    self.install_file(
        "data/com.system76.CosmicApplets.metainfo.xml", "usr/share/metainfo"
    )

    self.install_file(
        "cosmic-applet-status-area/data/dbus-1/com.system76.CosmicStatusNotifierWatcher.service",
        "usr/share/dbus-1/services",
    )
    self.install_file(
        "cosmic-applet-network/data/dbus-1/system.d/com.system76.CosmicSettings.Applet.NetworkManager.SecretAgent.conf",
        "usr/share/dbus-1/system.d",
    )

    self.install_license("LICENSE")
