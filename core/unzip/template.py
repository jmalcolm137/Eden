pkgname = "unzip"
pkgver = "6.0"
pkgrel = 0
# Oasis pkg/unzip (ver 6.0-29): unzip60 plus the Debian patch set.
build_style = "makefile"
make_build_target = "unzip"
make_build_args = [
    "-f",
    "unix/Makefile",
    "prefix=/usr",
    "LF2=",
    "L_BZ2=-lbz2",
]
make_use_env = True
makedepends = ["bzip2-devel"]
pkgdesc = "List, test and extract compressed files in a ZIP archive"
license = "Info-ZIP"
url = "http://infozip.sf.net"
source = "$(SOURCEFORGE_SITE)/infozip/unzip60.tar.gz"
sha256 = "036d96991646d0449ed0aa952e4fbe21b476ce994abc276e49d30e686708bd37"
# Oasis config.h enables bzip2, Unicode and large-file support
# no test target; upstream's suite needs a different source layout
options = ["!check"]


def init_build(self):
    self.cp(self.files_path / "config.h", ".")
    cfl = self.get_cflags(shell=True)
    ldfl = self.get_ldflags(shell=True)

    self.make_build_args += [
        "LOCAL_UNZIP=-include config.h",
        "CC=" + self.get_tool("CC"),
        "CFLAGS=" + cfl,
        "LFLAGS1=" + cfl + " " + ldfl,
    ]


def install(self):
    # Oasis installs only the main unzip tool and its manual page
    self.install_bin("unzip")
    self.install_man("man/unzip.1")
    self.install_license("LICENSE")
