pkgname = "aardvark-dns"
pkgver = "2.1.0"
pkgrel = 0
build_style = "cargo"
make_build_args = ["--bin", "aardvark-dns"]
hostmakedepends = ["cargo-bootstrap", "rust"]
pkgdesc = "Authoritative DNS server for Podman containers"
license = "Apache-2.0"
url = "https://github.com/containers/aardvark-dns"
source = f"{url}/archive/v{pkgver}/aardvark-dns-{pkgver}.tar.gz"
sha256 = "daf871488603e659b0501224cf0731ac317809b1d1701fc061cb4f6ae39a894f"
# the test suite needs a network namespace
options = ["!check"]


def install(self):
    self.install_file(
        f"target/{self.profile.triplet}/release/aardvark-dns",
        "usr/lib/podman",
        0o755,
    )
    self.install_license("LICENSE")
