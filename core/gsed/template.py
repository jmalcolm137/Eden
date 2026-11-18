pkgname = "gsed"
pkgver = "4.10"
pkgrel = 3
build_style = "gnu_configure"
configure_gen = []
makedepends = [
    "libatomic-chimera-devel-static",
    "linux-headers",
    "musl-devel-static",
]
pkgdesc = "GNU sed, installed as gsed"
license = "GPL-3.0-or-later"
url = "https://www.gnu.org/software/sed"
source = f"$(GNU_SITE)/sed/sed-{pkgver}.tar.xz"
sha256 = "b8e72182b2ec96a3574e2998c47b7aaa64cc20ce000d8e9ac313cc07cecf28c7"
tool_flags = {"LDFLAGS": ["-static-pie", "-unwindlib=none"]}
# no tests; keep the bootstrap build fast
options = ["bootstrap", "!check"]


def post_install(self):
    # the default sed is sbase's; keep GNU sed available under its own name
    # and behind the /usr/gnubin drop-in directory
    self.install_dir("usr/gnubin")
    (self.destdir / "usr/bin/sed").rename(self.destdir / "usr/bin/gsed")
    self.install_link("usr/gnubin/sed", "../bin/gsed")
    self.install_man("doc/sed.1", name="gsed")
    self.uninstall("usr/share/man/man1/sed.1")
    self.install_license("COPYING")
