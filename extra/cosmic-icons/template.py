pkgname = "cosmic-icons"
pkgver = "1.11.0"
pkgrel = 0
archs = ["x86_64"]
pkgdesc = "Icon theme for the COSMIC desktop environment"
license = "CC-BY-SA-4.0"
url = "https://github.com/pop-os/cosmic-icons"
source = f"https://github.com/pop-os/cosmic-icons/archive/refs/tags/epoch-{pkgver}.tar.gz"
sha256 = "1cbe6ca6ad3743a26b84ab17d3f7b8e5a885fcbcbb2d071ff0b74bccb5b44a53"
# data-only icon theme
options = ["!check"]


def install(self):
    root = self.destdir / "usr/share/icons/Cosmic"
    for sub in ["freedesktop", "extra"]:
        scalable = self.cwd / sub / "scalable"
        for path in scalable.rglob("*"):
            if path.is_file():
                rel = path.relative_to(self.cwd / sub)
                if (root / rel).exists():
                    continue
                self.install_file(
                    f"{sub}/{rel}", f"usr/share/icons/Cosmic/{rel.parent}"
                )

    self.install_file("index.theme", "usr/share/icons/Cosmic")
    self.install_license("LICENSE")
