pkgname = "xfwm4-themes"
pkgver = "4.20.0"
pkgrel = 0
pkgdesc = "Window manager themes used by the Xfce desktop"
license = "GPL-2.0-or-later"
url = "https://docs.xfce.org/xfce/xfwm4/start"
source = (
    f"https://archive.xfce.org/src/xfce/xfwm4/4.20/xfwm4-{pkgver}.tar.bz2"
)
sha256 = "a58b63e49397aa0d8d1dcf0636be93c8bb5926779aef5165e0852890190dcf06"
# only the theme data is shipped; the X11 window manager itself is not built
options = ["!check"]


def install(self):
    self.install_files("themes", "usr/share")
    self.install_license("COPYING")
