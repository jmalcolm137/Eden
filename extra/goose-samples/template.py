pkgname = "goose-samples"
pkgver = "2026.4"
pkgrel = 0
depends = ["goose"]
pkgdesc = "Documentation and sample programs for the Goose language"
license = "Apache-2.0"
url = "https://aardappel.github.io/goose"
source = f"https://github.com/aardappel/goose/archive/refs/tags/v{pkgver}.tar.gz"
sha256 = "943d785fb191de7b52539e9cf16715701babcacd339323f786729c2132343d9b"
# data-only package; keep the docs with the samples
options = ["!check", "!splitdoc"]


def install(self):
    self.install_files("docs", "usr/share/doc", name="goose-samples")
    self.install_files("samples", "usr/share/goose")
    self.install_license("LICENSE")
