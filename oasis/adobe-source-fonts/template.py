pkgname = "adobe-source-fonts"
pkgver = "3.028"
pkgrel = 0
pkgdesc = "Adobe Source Sans, Serif, and Code Pro fonts from Oasis"
license = "OFL-1.1"
url = "https://github.com/adobe-fonts"
source = [
    "https://github.com/adobe-fonts/source-sans/archive/3.028R.tar.gz",
    "https://github.com/adobe-fonts/source-serif/archive/4.004R.tar.gz",
    "https://github.com/adobe-fonts/source-code-pro/archive/"
    "2.038R-ro/1.058R-it/1.018R-VAR.tar.gz",
]
source_paths = ["sans", "serif", "codepro"]
sha256 = [
    "23df371ce8ce0c5c57e750f1b01af6a31e437fe1737df0501b8181162642686a",
    "dfb364735699cb830caad534cf7741234804d28e4b6fc5e4736b2401f6131aba",
    "d8f879fefd66ecb7291ea2d73984b9c0a97fb499424e58290ba6b81787d0c725",
]
# fonts only, no tests
options = ["!check"]


def install(self):
    for src in sorted((self.cwd / "sans/OTF").glob("*.otf")):
        self.install_file(f"sans/OTF/{src.name}", "usr/share/fonts")
    for src in sorted((self.cwd / "serif/OTF").glob("*.otf")):
        self.install_file(f"serif/OTF/{src.name}", "usr/share/fonts")
    for src in sorted((self.cwd / "codepro/OTF").glob("*.otf")):
        self.install_file(f"codepro/OTF/{src.name}", "usr/share/fonts")

    self.install_license("sans/LICENSE.md", name="LICENSE.sans.md")
    self.install_license("serif/LICENSE.md", name="LICENSE.serif.md")
    self.install_license("codepro/LICENSE.md", name="LICENSE.code.md")
