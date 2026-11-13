pkgname = "iproute2"
pkgver = "6.8.0"
pkgrel = 1
build_style = "makefile"
make_build_args = ["CC=clang", "HOSTCC=clang"]
make_build_env = {
    "CC": "clang",
    "HOSTCC": "clang",
    "PREFIX": "/usr",
    "SBINDIR": "/usr/bin",
    "LIBDIR": "/usr/lib",
    "CONFDIR": "/etc/iproute2",
    "NETNS_RUN_DIR": "/run/netns",
    "NETNS_ETC_DIR": "/etc/netns",
    "HAVE_ELF": "n",
    "YACC": "byacc",
}
make_install_args = ["CC=clang", "HOSTCC=clang"]
make_install_env = dict(make_build_env)
make_use_env = True
makedepends = ["byacc", "flex", "linux-headers", "m4"]
pkgdesc = "IP routing utilities"
license = "GPL-2.0-or-later"
url = "https://www.kernel.org/pub/linux/utils/net/iproute2"
source = f"{url}/iproute2-{pkgver}.tar.xz"
sha256 = "03a6cca3d71a908d1f15f7b495be2b8fe851f941458dc4664900d7f45fcf68ce"
tool_flags = {"CFLAGS": ["-include", "sys/time.h"]}
# no test suite in the Oasis recipe
options = ["etcfiles", "!check"]


def pre_build(self):
    p = self.cwd / "Makefile"
    text = p.read_text()
    text = text.replace(
        "find etc/iproute2 -maxdepth 1 -type f",
        "find etc/iproute2 -type f",
    )
    p.write_text(text)


def post_install(self):
    self.uninstall("usr/share/bash-completion", missing_ok=True)

