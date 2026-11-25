pkgname = "protoc-bootstrap"
pkgver = "36.2"
pkgrel = 0
archs = ["x86_64"]
pkgdesc = "Protocol Buffers compiler bootstrap binaries"
license = "BSD-3-Clause"
url = "https://protobuf.dev"
source = (
    "https://github.com/protocolbuffers/protobuf/releases/download/"
    f"v{pkgver}/protoc-{pkgver}-linux-x86_64.zip"
)
sha256 = "121f6c7afe1d4d0e3ea6aab9432038599250134cbf4474cb1167d2c7decd4278"
# prebuilt upstream binaries
options = ["!check", "!strip"]


def install(self):
    self.install_bin("bin/protoc")
    self.install_files(self.cwd / "include", "usr")
    self.install_license(self.files_path / "LICENSE")
