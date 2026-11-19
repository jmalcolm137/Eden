pkgname = "bash"
pkgver = "5.3"
pkgrel = 0
build_style = "gnu_configure"
configure_args = [
    "--without-bash-malloc",
    "--with-installed-readline=no",
]
configure_gen = []
hostmakedepends = ["gmake"]
pkgdesc = "GNU Bourne Again Shell"
license = "GPL-3.0-or-later"
url = "https://www.gnu.org/software/bash"
source = f"$(GNU_SITE)/bash/bash-{pkgver}.tar.gz"
sha256 = "0d5cd86965f869a26cf64f4b71be7b96f90a3ba8b3d74e27e8e9d9d5550f31ba"
tool_flags = {"CFLAGS": ['-DSYS_BASHRC="/usr/share/bash/bashrc"']}
# the testsuite takes very long and needs a full interactive environment
options = ["!check"]


def post_install(self):
    self.uninstall("usr/lib", missing_ok=True)
    self.uninstall("usr/include", missing_ok=True)
    self.install_shell("/usr/bin/bash")
