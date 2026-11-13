pkgname = "man-pages-posix"
pkgver = "2017a"
pkgrel = 0
pkgdesc = "POSIX man pages"
license = "custom:posix"
url = "https://pubs.opengroup.org/onlinepubs/9699919799/nframe.html"
source = (
    "https://www.kernel.org/pub/linux/docs/man-pages/man-pages-posix/"
    f"man-pages-posix-{pkgver[:-1]}-{pkgver[-1]}.tar.gz"
)
sha256 = "8ba538e91db62622c507e34899e1e7d560e870505c00cd4d7f8d5048e54d056e"
# data-only package
options = ["!autosplit", "!check"]


def install(self):
    self.install_license("POSIX-COPYRIGHT")
    for line in (self.files_path / "manpages.txt").read_text().splitlines():
        line = line.strip()
        if not line or line.startswith("#"):
            continue
        section = line.rsplit(".", 1)[1]
        self.install_file(line, f"usr/share/man/man{section}")
