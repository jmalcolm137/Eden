pkgname = "yt-dlp"
pkgver = "2026.10.21"
pkgrel = 0
depends = ["python"]
pkgdesc = "CLI program to download videos from YouTube and other sites"
license = "Unlicense"
url = "https://github.com/yt-dlp/yt-dlp"
source = f"{url}/releases/download/{pkgver}/yt-dlp.tar.gz"
sha256 = "5f1e419f76e49c996061511ef9eacce50d4aa4959c34480539562e9e1295708d"
# no test suite in the Oasis recipe
options = ["!check"]


def init_configure(self):
    self.python_version = "3.15"


def install(self):
    self.install_bin(self.files_path / "yt-dlp")
    self.install_man("yt-dlp.1")
    self.install_license("LICENSE")

    for line in (self.files_path / "pylibs.txt").read_text().splitlines():
        line = line.strip()
        if not line or line.startswith("#"):
            continue
        dest = "usr/lib/python3.15/" + line.rsplit("/", 1)[0]
        self.install_file(line, dest)
