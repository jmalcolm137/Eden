pkgname = "pop-launcher"
pkgver = "1.11.0"
pkgrel = 0
archs = ["x86_64"]
hostmakedepends = ["cargo-bootstrap", "git", "pkgconf", "rust"]
makedepends = ["dbus-devel", "libxkbcommon-devel", "llvm-devel", "mesa-devel"]
pkgdesc = "Modular IPC-based desktop launcher service"
license = "MPL-2.0"
url = "https://github.com/pop-os/launcher"
source = f"https://github.com/pop-os/launcher/archive/refs/tags/epoch-{pkgver}.tar.gz"
sha256 = "5c36c3304c48c047b5b6a1ae645f0ceb44447aec82db862fb93be6184af3fdc7"
# the test suite needs a running session
options = ["!check"]

_cargo_env = {
    "CARGO_HOME": "/cbuild_cache/cargo",
    "CARGO_NET_OFFLINE": "true",
    "LIBCLANG_PATH": "/usr/lib",
}

_plugins = [
    "calc",
    "cosmic_toplevel",
    "desktop_entries",
    "files",
    "find",
    "pop_shell",
    "pulse",
    "recent",
    "scripts",
    "terminal",
    "web",
]


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
        "-p",
        "pop-launcher-bin",
        env=_cargo_env,
    )


def install(self):
    self.install_bin("target/release/pop-launcher-bin", name="pop-launcher")

    for plugin in _plugins:
        dest = f"usr/lib/pop-launcher/plugins/{plugin}"
        for path in (self.cwd / "plugins/src" / plugin).glob("*.ron"):
            self.install_file(f"plugins/src/{plugin}/{path.name}", dest)
        self.install_link(f"{dest}/{plugin.replace('_', '-')}", "../../../../bin/pop-launcher")

    scripts = self.cwd / "scripts"
    self.install_dir("usr/lib/pop-launcher/scripts")
    for path in scripts.iterdir():
        self.do(
            "cp",
            "-a",
            f"scripts/{path.name}",
            f"{self.chroot_destdir}/usr/lib/pop-launcher/scripts/",
        )

    self.install_license("LICENSE")
