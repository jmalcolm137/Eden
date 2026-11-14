pkgname = "terminus-font"
pkgver = "4.49.1"
pkgrel = 0
pkgdesc = "Terminus bitmap fonts"
license = "OFL-1.1"
url = "https://terminus-font.sourceforge.net"
source = (
    "https://downloads.sourceforge.net/project/terminus-font/"
    "terminus-font-4.49/terminus-font-4.49.1.tar.gz"
)
sha256 = "d961c1b781627bf417f9b340693d64fc219e0113ad3a3af1a3424c7aa373ef79"
# no test suite in the Oasis recipe
options = ["!check"]

_sizes = [12, 14, 16, 20, 22, 24, 28, 32]


def build(self):
    self.mkdir("out", parents=True)
    self.cp(self.files_path / "ucstoany.awk", "ucstoany.awk")
    for size in _sizes:
        for weight in ("n", "b"):
            font = f"ter-u{size}{weight}.bdf"
            out = f"out/{font}"
            self.do(
                "sh",
                "-c",
                f"awk -v font={font} -v charset=ISO10646-1 "
                f"-f ucstoany.awk uni/x11gr.uni uni/10646-1.uni {font} > {out} || true",
            )


def install(self):
    self.install_dir("usr/share/fonts/terminus")
    for size in _sizes:
        for weight in ("n", "b"):
            self.install_file(
                f"out/ter-u{size}{weight}.bdf", "usr/share/fonts/terminus"
            )
    self.install_license("COPYING")
