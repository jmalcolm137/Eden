pkgname = "fakeroot"
pkgver = "2.1.4"
pkgrel = 2
build_style = "meson"
configure_args = [
    "-Dipc=sysv",
    "-Ddbformat=inode",
    "-Ddocs=false",
]
hostmakedepends = ["muon", "python", "samurai"]
makedepends = ["acl-devel", "libcap-devel"]
checkdepends = ["ugetopt"]
depends = [self.with_pkgver("fakeroot-core")]
pkgdesc = "Tool for simulating superuser privileges"
license = "GPL-3.0-or-later"
url = "https://salsa.debian.org/clint/fakeroot"
source = f"{url}/-/archive/upstream/{pkgver}/fakeroot-upstream-{pkgver}.tar.gz"
sha256 = "b71f645037e5a44a474efd641b353b506db3803eb60ed90a4ac6322a8d96d340"
# tests need a working fakeroot, which does not exist in the stage-0 root
options = ["bootstrap", "!check"]

if self.stage > 0:
    depends += ["ugetopt"]


@subpackage("fakeroot-core")
def _(self):
    self.subdesc = "core"

    return ["usr/bin/faked", "usr/lib"]
