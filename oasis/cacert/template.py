pkgname = "cacert"
pkgver = "2026.10.20"
pkgrel = 0
pkgdesc = "CA certificate bundle"
license = "MPL-2.0"
url = "https://curl.se/ca"
source = "!https://curl.se/ca/cacert-2026-10-20.pem>cacert.pem"
sha256 = "796f1389bfea13c0ed78f663b765baaff54a508e5483786bd6ece73c5e3e3cbe"
# data-only package
options = ["!check"]


def install(self):
    self.install_file(self.sources_path / "cacert.pem", "usr/share/cacert", name="cert.pem")
