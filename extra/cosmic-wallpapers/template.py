pkgname = "cosmic-wallpapers"
pkgver = "1.11.0"
pkgrel = 0
archs = ["x86_64"]
pkgdesc = "Wallpapers for the COSMIC desktop environment"
license = "CC-BY-SA-4.0"
url = "https://github.com/pop-os/cosmic-wallpapers"
source = f"https://github.com/pop-os/cosmic-wallpapers/archive/refs/tags/epoch-{pkgver}.tar.gz"
sha256 = "3bc7580caabef7e42c161180bc1a27095962c377acbde7ec0ee4d8da130e7857"
# data-only package
options = ["!check"]


def install(self):
    for path in (self.cwd / "original").iterdir():
        if path.is_file():
            self.install_file(
                f"original/{path.name}", "usr/share/backgrounds/cosmic"
            )

    self.install_license("LICENSE")
