pkgname = "gnu-compat"
pkgver = "0.1"
pkgrel = 0
build_style = "meta"
depends = [
    "gmake",
    "gnu-m4",
    "gsed",
    "uutils-coreutils",
    "uutils-findutils",
]
pkgdesc = "GNU tool names in the /usr/gnubin drop-in directory"
license = "custom:meta"
url = "https://eden-linux.org"
# the symlinks point at tools provided by the dependencies above
options = ["brokenlinks"]


def install(self):
    self.install_dir("usr/gnubin")
    self.install_link("usr/gnubin/make", "../bin/gmake")
    self.install_link("usr/gnubin/sed", "../bin/gsed")
    self.install_link("usr/gnubin/m4", "../bin/gm4")
