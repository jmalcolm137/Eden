pkgname = "distrobox"
pkgver = "1.8.2.6"
pkgrel = 0
depends = ["podman"]
pkgdesc = "Use any Linux distribution inside your terminal"
license = "GPL-3.0-only"
url = "https://github.com/89luca89/distrobox"
source = f"{url}/archive/refs/tags/{pkgver}.tar.gz"
sha256 = "693c85f44720f9c2be8691141eaa1dc2773ee37e63ae02fff8b838dcf54c413e"
# the test suite provisions containers
# the zsh completion ships private helper functions (_distrobox_containers,
# _distrobox_images, ...) that are not commands; cbuild would flag them
options = ["!check", "!lintcomp"]


def install(self):
    # the main command and the per-command entry points are POSIX sh scripts
    for f in self.cwd.glob("distrobox*"):
        if f.is_file():
            self.install_bin(f)

    for f in (self.cwd / "man" / "man1").glob("*.1"):
        self.install_man(f)
    for f in (self.cwd / "completions" / "bash").glob("*"):
        self.install_file(f, "usr/share/bash-completion/completions")
    for f in (self.cwd / "completions" / "zsh").glob("*"):
        self.install_file(f, "usr/share/zsh/site-functions")

    icon = self.cwd / "icons"
    self.install_file(
        icon / "terminal-distrobox-icon.svg",
        "usr/share/icons/hicolor/scalable/apps",
    )
    for size in (16, 22, 24, 32, 36, 48, 64, 72, 96, 128, 256):
        self.install_file(
            icon / "hicolor" / f"{size}x{size}" / "apps"
            / "terminal-distrobox-icon.png",
            f"usr/share/icons/hicolor/{size}x{size}/apps",
        )

    self.install_license("COPYING.md")
