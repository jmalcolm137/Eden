pkgname = "acpid"
pkgver = "2.0.34"
pkgrel = 0
build_style = "gnu_configure"
configure_args = ["--disable-nls"]
configure_gen = []
makedepends = ["linux-headers"]
pkgdesc = "ACPI event daemon"
license = "GPL-2.0-or-later"
url = "https://sourceforge.net/projects/acpid2"
source = "https://downloads.sourceforge.net/project/acpid2/acpid-2.0.34.tar.xz"
sha256 = "2d095c8cfcbc847caec746d62cdc8d0bff1ec1bc72ef7c674c721e04da6ab333"
tool_flags = {"CFLAGS": ["-D_GNU_SOURCE", "-D_LARGEFILE64_SOURCE"]}
# no test suite in the Oasis recipe
options = ["etcfiles", "!check"]
