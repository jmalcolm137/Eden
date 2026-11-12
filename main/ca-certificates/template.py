pkgname = "ca-certificates"
pkgver = "20261020"
pkgrel = 1
pkgdesc = "CA certificate bundle from Oasis cacert"
license = "MPL-2.0"
url = "https://curl.se/ca"
source = "!https://curl.se/ca/cacert-2026-10-20.pem>cacert-2026-10-20.pem"
sha256 = "796f1389bfea13c0ed78f663b765baaff54a508e5483786bd6ece73c5e3e3cbe"
# no tests; this installs a static bundle instead of running update scripts
options = ["etcfiles", "!check", "bootstrap"]


def install(self):
    self.install_dir("etc/ssl/certs")
    self.install_file(
        self.sources_path / "cacert-2026-10-20.pem",
        "etc/ssl/certs",
        name="ca-certificates.crt",
    )
    self.install_file(
        self.sources_path / "cacert-2026-10-20.pem",
        "usr/share/cacert",
        name="cert.pem",
    )
