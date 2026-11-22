pkgname = "cosmic-session"
pkgver = "1.11.0"
pkgrel = 0
archs = ["x86_64"]
hostmakedepends = ["cargo-bootstrap", "git", "rust"]
depends = ["dbus", "perp"]
pkgdesc = "Session manager for the COSMIC desktop environment"
license = "GPL-3.0-only"
url = "https://github.com/pop-os/cosmic-session"
source = f"https://github.com/pop-os/cosmic-session/archive/refs/tags/epoch-{pkgver}.tar.gz"
sha256 = "0c3d3e1f0ef534a063621932cdcc15c8af258df5c12ce6023615dc33222ebca5"
# the test suite needs a running session bus and compositor
options = ["!check", "etcfiles"]

_cargo_env = {
    "CARGO_HOME": "/cbuild_cache/cargo",
    "CARGO_NET_OFFLINE": "true",
}


def post_patch(self):
    # systemd is not used on Eden.  Besides removing the systemctl calls,
    # create the per-user runtime directory that logind would normally own so
    # that the session can be started straight from a TTY.
    p = self.cwd / "data/start-cosmic"
    text = p.read_text()

    anchor = "# use the user's preferred shell"
    i = text.index(anchor)
    j = text.rindex("if command -v systemctl", 0, i)
    text = text[:j] + text[i:]

    anchor = "# Run cosmic-session"
    i = text.index(anchor)
    j = text.rindex("if command -v systemctl", 0, i)
    removed = text[j:i]
    if "systemctl --user import-environment" not in removed:
        self.error("unexpected start-cosmic systemd block")
    text = text[:j] + text[i:]

    old = "set -e\n"
    new = """set -e

# No systemd-logind here, so create the per-user runtime directory ourselves.
: "${XDG_RUNTIME_DIR:=/run/user/$(id -u)}"
if [ ! -d "$XDG_RUNTIME_DIR" ]; then
    mkdir -p "$XDG_RUNTIME_DIR"
    chmod 700 "$XDG_RUNTIME_DIR"
fi
"""
    if old not in text:
        self.error("unexpected start-cosmic prologue")
    p.write_text(text.replace(old, new, 1))


def prepare(self):
    self.do(
        "cargo",
        "fetch",
        "--locked",
        env={"CARGO_HOME": "/cbuild_cache/cargo"},
        allow_network=True,
    )


def build(self):
    # The systemd and logind features are not usable on Eden.  Keep the
    # freedesktop autostart handling, which cosmic-session runs itself when
    # systemd is absent.
    self.do(
        "cargo",
        "build",
        "--release",
        "--locked",
        "--no-default-features",
        "--features",
        "autostart",
        env=_cargo_env,
    )


def install(self):
    self.install_bin("target/release/cosmic-session")
    self.install_bin("data/start-cosmic")

    self.install_file("data/cosmic-mimeapps.list", "usr/share/applications")
    self.install_file("data/cosmic.desktop", "usr/share/wayland-sessions")
    self.install_file("data/dconf/profile/cosmic", "usr/share/dconf/profile")

    self.install_file(
        self.files_path / "perp/cosmic-session/rc.main",
        "etc/perp/cosmic-session",
        mode=0o755,
    )

    self.install_license("LICENSE.md")


def post_install(self):
    # The sticky bit marks the service as active for perpd.
    (self.destdir / "etc/perp/cosmic-session").chmod(0o1755)
