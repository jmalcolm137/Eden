pkgname = "netavark"
pkgver = "2.1.0"
pkgrel = 0
build_style = "cargo"
make_build_args = ["--bin", "netavark"]
hostmakedepends = [
    "cargo-bootstrap",
    "go-md2man",
    "protoc-bootstrap",
    "rust",
]
pkgdesc = "Container network stack for Podman"
license = "Apache-2.0"
url = "https://github.com/containers/netavark"
source = f"{url}/archive/v{pkgver}/netavark-{pkgver}.tar.gz"
sha256 = "96677048168ddd1abe313e4c2e17f1cace72b60ee1bac8ca12a4bd7dfcadfbbb"
# the test suite needs root and a network namespace
options = ["!check"]


def install(self):
    self.do("go-md2man", "-in", "docs/netavark.1.md", "-out", "netavark.1")
    self.install_man("netavark.1")
    self.install_file(
        f"target/{self.profile.triplet}/release/netavark", "usr/lib/podman", 0o755
    )
    self.install_license("LICENSE")
