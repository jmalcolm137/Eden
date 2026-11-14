pkgname = "bubblewrap"
pkgver = "0.11.0"
pkgrel = 2
# Oasis pkg/bubblewrap/src
_commit = "9ca3b05ec787acfb4b17bed37db5719fa777834f"
makedepends = ["linux-headers"]
pkgdesc = "Unprivileged sandboxing tool"
license = "LGPL-2.0-or-later"
url = "https://github.com/containers/bubblewrap"
source = f"{url}/archive/{_commit}.tar.gz"
sha256 = "552cec9c79bb85c8ecd25ae3e55efca9af03390c17d829885ee45722dedada4f"
# no test suite in the Oasis recipe
options = ["bootstrap", "!check"]

_cflags = ["-std=c11", "-Wall", "-Wpedantic", "-Wvla", "-D_GNU_SOURCE", "-I."]


def pre_build(self):
    self.cp(self.files_path / "config.h", "config.h")
    self.cp(self.files_path / "caps.c", "caps.c")
    self.cp(self.files_path / "caps.awk", "caps.awk")
    self.cp(self.files_path / "bwrap.1", "bwrap.1")
    self.do(
        "sh",
        "-c",
        "awk -f "
        + "caps.awk"
        + " /usr/include/linux/capability.h > caps.h",
    )


def build(self):
    from cbuild.util import compiler

    cc = compiler.C(self)
    cc.invoke(
        ["bubblewrap.c", "bind-mount.c", "network.c", "utils.c", "caps.c"],
        "bwrap",
        flags=_cflags,
    )


def install(self):
    self.install_bin("bwrap")
    self.install_man("bwrap.1")
    self.install_license("COPYING")
