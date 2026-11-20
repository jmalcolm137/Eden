pkgname = "udev"
pkgver = "3.2.14"
pkgrel = 2
build_style = "gnu_configure"
configure_args = [
    "--disable-blkid",
    "--disable-hwdb",
    "--disable-kmod",
    "--disable-manpages",
    "--disable-mtd-probe",
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
options = ["etcfiles", "!check"]


@subpackage("udev-devel")
def _(self):
    return self.default_devel()


def post_install(self):
    # upstream installs the same file in two pkgconfig directories
    self.uninstall("usr/share/pkgconfig/udev.pc", missing_ok=True)
    self.install_license("COPYING")
