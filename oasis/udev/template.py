pkgname = "udev"
pkgver = "3.2.14"
pkgrel = 1
build_style = "gnu_configure"
configure_args = [
    "--disable-blkid",
    "--disable-hwdb",
    "--disable-kmod",
    "--disable-manpages",
    "--disable-mtd-probe",
    "--disable-programs",
    "--disable-rule-generator",
    "--disable-selinux",
]
hostmakedepends = ["autoconf", "automake", "gperf", "libtool", "pkgconf"]
makedepends = ["linux-headers"]
pkgdesc = "Device enumeration library from eudev"
license = "LGPL-2.1-or-later"
url = "https://github.com/eudev-project/eudev"
source = "https://github.com/eudev-project/eudev/archive/refs/tags/v3.2.14.tar.gz"
sha256 = "c340e6c51dfc5531ac0c0fa84a34b72162acf525f9023eb9cf4931b782c8f177"
# tests need a running udev
options = ["!check"]


@subpackage("udev-devel")
def _(self):
    return self.default_devel()


def post_install(self):
    pc = self.destdir / "usr/lib/pkgconfig/udev.pc"
    pc.write_text(
        "Name: udev\n"
        "Description: udev\n"
        "Version: 3.2.14\n"
        "Requires: libudev\n"
        "udev_dir=/usr/lib/udev\n"
    )
    self.install_license("COPYING")
