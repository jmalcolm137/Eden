pkgname = "xdg-desktop-portal-cosmic"
pkgver = "1.11.0"
pkgrel = 0
archs = ["x86_64"]
hostmakedepends = ["cargo-bootstrap", "git", "pkgconf", "rust"]
makedepends = [
    "clang-libs",
    "glib-devel",
    "gst-plugins-base-devel",
    "gstreamer-devel",
    "libxkbcommon-devel",
    "llvm-devel",
    "mesa-devel",
    "pipewire-devel",
    "wayland-devel",
]
depends = ["cosmic-icons"]
pkgdesc = "Xdg-desktop-portal implementation for COSMIC"
license = "GPL-3.0-only"
url = "https://github.com/pop-os/xdg-desktop-portal-cosmic"
source = f"https://github.com/pop-os/xdg-desktop-portal-cosmic/archive/refs/tags/epoch-{pkgver}.tar.gz"
sha256 = "5befa4beda6ee231ebaa553b3db53d794500b5646de385fd1f576a7406242f16"
# the test suite needs a running session
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


def post_patch(self):
    # D-Bus activation is used instead of a systemd user unit.
    appid = "org.freedesktop.impl.portal.desktop.cosmic"
    p = self.cwd / "data/dbus-1" / f"{appid}.service.in"
    text = p.read_text().replace("@libexecdir@", "/usr/lib")
    (p.parent / f"{appid}.service").write_text(text)


def build(self):
    self.do(
        "cargo",
        "build",
        "--release",
        "--locked",
        "--bin",
        "xdg-desktop-portal-cosmic",
        env=_cargo_env,
    )


def install(self):
    self.install_file(
        "target/release/xdg-desktop-portal-cosmic", "usr/lib", mode=0o755
    )

    self.install_file(
        "data/dbus-1/org.freedesktop.impl.portal.desktop.cosmic.service",
        "usr/share/dbus-1/services",
    )
    self.install_file(
        "data/cosmic.portal", "usr/share/xdg-desktop-portal/portals"
    )
    self.install_file(
        "data/cosmic-portals.conf", "usr/share/xdg-desktop-portal"
    )

    icons = self.cwd / "data/icons"
    for path in icons.rglob("*"):
        if path.is_file():
            rel = path.relative_to(icons)
            self.install_file(
                f"data/icons/{rel}", f"usr/share/icons/hicolor/{rel.parent}"
            )

    self.install_license("LICENSE")
