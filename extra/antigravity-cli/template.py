pkgname = "antigravity-cli"
pkgver = "1.5.13"
pkgrel = 1
# Google ships this only as prebuilt static binaries; the repository has no
# source. Upstream publishes musl builds, which is what we install here.
pkgdesc = "Google Antigravity agent harness for the terminal"
license = "custom:proprietary"
url = "https://antigravity.google/product/antigravity-cli"
match self.profile.arch:
    case "x86_64":
        source = (
            "https://github.com/google-antigravity/antigravity-cli/"
            f"releases/download/{pkgver}/agy_cli_linux_x64_musl.tar.gz"
        )
        sha256 = "b63da7a01384ad289dd03e21a2fe8a7d8213f2a2588bd743d683f9a7441b8291"
    case "aarch64":
        source = (
            "https://github.com/google-antigravity/antigravity-cli/"
            f"releases/download/{pkgver}/agy_cli_linux_arm64_musl.tar.gz"
        )
        sha256 = "a03ff48b207f5076057fde69e4fb38f9ba3d35fabfa6a5dfb9f89e850917501e"
    case _:
        broken = f"no Antigravity CLI build for {self.profile.arch}"
# prebuilt, already stripped
options = ["!check", "!distlicense", "!strip"]


def install(self):
    self.install_bin("antigravity")
    # the documented command name
    self.install_link("usr/bin/agy", "antigravity")
