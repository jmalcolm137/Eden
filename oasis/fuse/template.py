pkgname = "fuse"
pkgver = "3.10.5"
pkgrel = 2
build_style = "meson"
configure_args = [
    "-Dutils=false",
    "-Dexamples=false",
    "-Dtests=false",
    "-Ddefault_library=shared",
]
makedepends = ["linux-headers"]
pkgdesc = "Filesystem in Userspace"
license = "LGPL-2.1-or-later"
url = "https://github.com/libfuse/libfuse"
source = f"{url}/releases/download/fuse-{pkgver}/fuse-{pkgver}.tar.xz"
sha256 = "b2e283485d47404ac896dd0bb7f7ba81e1470838e677e45f659804c3a3b69666"
tool_flags = {"CFLAGS": ["-UHAVE_SYMVER_ATTRIBUTE"], "LDFLAGS": ["-Wl,--undefined-version"]}
# no test suite in the Oasis recipe
options = ["!check"]


def pre_configure(self):
    p = self.cwd / "lib/fuse_misc.h"
    p.write_text(p.read_text().replace("#ifndef __APPLE__", "#if 0", 1))



@subpackage("fuse-devel")
def _(self):
    return self.default_devel()
