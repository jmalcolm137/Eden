pkgname = "hostapd"
pkgver = "2.11"
pkgrel = 0
makedepends = ["libnl", "libnl-devel", "linux-headers"]
pkgdesc = "IEEE 802.11 AP and IEEE 802.1X/WPA/WPA2/EAP authenticator"
license = "BSD-3-Clause"
url = "https://w1.fi/hostapd"
source = f"https://w1.fi/releases/hostapd-{pkgver}.tar.gz"
sha256 = "2b3facb632fd4f65e32f4bf82a76b4b72c501f995a4f62e330219fe7aed1747a"
# no test suite in the Oasis recipe
options = ["etcfiles", "!check"]


def pre_build(self):
    self.cp(self.files_path / "defconfig", "hostapd/.config")


def build(self):
    self.do(
        "gmake",
        "-C",
        "hostapd",
        "CC=clang",
        f"-j{self.make_jobs}",
    )


def install(self):
    self.install_bin("hostapd/hostapd")
    self.install_bin("hostapd/hostapd_cli")
    self.install_file(self.files_path / "hostapd.conf", "etc/hostapd")
    self.install_license("COPYING")
