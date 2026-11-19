pkgname = "linux-firmware"
pkgver = "20261019"
pkgrel = 0
archs = ["x86_64"]
pkgdesc = "Firmware files for Linux"
license = "custom:WHENCE"
url = "https://gitlab.com/kernel-firmware/linux-firmware"
source = (
    "https://gitlab.com/kernel-firmware/linux-firmware/-/archive/"
    f"{pkgver}/linux-firmware-{pkgver}.tar.gz"
)
sha256 = "1e80b924afc2e78096361d58953a281f6fa8a5f6a7622f9a053004ff9cb9ac09"
# no test suite
options = ["!check", "keepempty"]


def install(self):
    self.install_dir("usr/lib/firmware")
    self.do(
        "cp",
        "-a",
        ".",
        f"{self.chroot_destdir}/usr/lib/firmware/",
    )
    self.uninstall("usr/lib/firmware/.git", missing_ok=True)
    self.install_file("WHENCE", "usr/share/licenses/linux-firmware")


@subpackage("linux-firmware-broadcom")
def _(self):
    self.subdesc = "Broadcom firmware"
    return ["usr/lib/firmware/brcm"]


@subpackage("linux-firmware-amdgpu")
def _(self):
    self.subdesc = "AMD GPU firmware"
    return ["usr/lib/firmware/amdgpu"]


@subpackage("linux-firmware-intel")
def _(self):
    self.subdesc = "Intel firmware"
    return ["usr/lib/firmware/i915", "usr/lib/firmware/intel", "usr/lib/firmware/iwlwifi*"]


@subpackage("linux-firmware-nvidia")
def _(self):
    self.subdesc = "NVIDIA firmware"
    return ["usr/lib/firmware/nvidia"]


@subpackage("linux-firmware-radeon")
def _(self):
    self.subdesc = "Radeon firmware"
    return ["usr/lib/firmware/radeon"]
