pkgname = "usbids"
pkgver = "2020.08.26"
pkgrel = 0
# Oasis pkg/usbids/src
_commit = "075e753cd7d7784f597b998f97c056bbc3472f9b"
pkgdesc = "USB vendor and device ID database"
license = "GPL-3.0-or-later"
url = "https://github.com/usbids/usbids"
source = f"{url}/archive/{_commit}.tar.gz"
sha256 = "8197196250c5649f0bd2d95db8805fb97213581fe8e1fd61351df421455ec519"
# data-only package
options = ["!check"]


def install(self):
    self.install_file("usb.ids", "usr/share/misc")
    self.install_license("LICENSE")
