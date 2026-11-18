pkgname = "autoconf"
pkgver = "2.73"
pkgrel = 0
build_style = "gnu_configure"
configure_env = {"M4": "/usr/bin/m4"}
configure_gen = []
hostmakedepends = ["m4", "perl"]
depends = ["cmd:awk!base-files", "m4", "perl"]
pkgdesc = "Generates automatic source code configuration scripts"
license = "GPL-3.0-or-later"
url = "https://www.gnu.org/software/autoconf"
source = f"https://ftp.gnu.org/gnu/autoconf/autoconf-{pkgver}.tar.gz"
sha256 = "259ddfa3bddc799cfb81489cc0f17dfdf1bd6d1505dda53c0f45ff60d6a4f9a7"
# tests are not needed for a build tool
options = ["!check"]
