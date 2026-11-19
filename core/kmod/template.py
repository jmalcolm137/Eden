pkgname = "kmod"
pkgver = "34.2"
pkgrel = 1
build_style = "meson"
configure_args = [
    "-Dxz=enabled",
    "-Dzstd=enabled",
    "-Dzlib=enabled",
    "-Dopenssl=disabled",
    "-Dmanpages=false",
    "-Ddocs=false",
    "-Dbashcompletiondir=no",
    "-Dfishcompletiondir=no",
    "-Dzshcompletiondir=no",
]
hostmakedepends = ["muon", "pkgconf", "samurai"]
makedepends = ["xz-devel", "zlib-static", "zstd-devel"]
depends = ["ubase"]
pkgdesc = "Linux kernel module handling"
license = "GPL-2.0-or-later AND LGPL-2.1-or-later"
url = "https://git.kernel.org/pub/scm/utils/kernel/kmod/kmod.git"
source = f"$(KERNEL_SITE)/utils/kernel/kmod/kmod-{pkgver}.tar.gz"
sha256 = "d60a79fb12a85feab75674ce5b86b2c8bae1714f775f481eae926bd2657b2ffe"
# no meaningful check target
options = ["!check"]


def post_install(self):
    # ubase provides these; keep its binaries
    for f in ["usr/bin/insmod", "usr/bin/lsmod", "usr/bin/rmmod"]:
        self.uninstall(f, missing_ok=True)
    self.install_file(
        self.files_path / "depmod-search.conf",
        "usr/lib/depmod.d",
        name="search.conf",
    )
    self.install_tmpfiles(self.files_path / "tmpfiles.conf")
    self.install_license("COPYING")


@subpackage("kmod-devel")
def _(self):
    return self.default_devel()
