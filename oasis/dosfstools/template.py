pkgname = "dosfstools"
pkgver = "4.2"
pkgrel = 1
# Oasis pkg/dosfstools/src
_commit = "697f7692c951173c1b732901e13f72bd3182d575"
makedepends = ["linux-headers"]
pkgdesc = "DOS filesystem utilities"
license = "GPL-3.0-or-later"
url = "https://github.com/dosfstools/dosfstools"
source = f"{url}/archive/{_commit}.tar.gz"
sha256 = "de79efb06c3b419a6d809c9e8b01e9cd80adaa0d5d642e9de6b49196e5c70e83"
# no test suite in the Oasis recipe
options = ["!check"]

_cflags = [
    "-std=c99",
    "-Wall",
    "-Wpedantic",
    "-Wno-address-of-packed-member",
    "-Wno-overflow",
    "-D_GNU_SOURCE",
    "-include",
    "config.h",
    "-I.",
    "-Isrc/blkdev",
]


def pre_build(self):
    self.cp(self.files_path / "config.h", "config.h")
    self.cp(self.files_path / "version.h", "version.h")
    for man in ("fsck.fat.8", "mkfs.fat.8"):
        text = (self.cwd / f"manpages/{man}.in").read_text()
        (self.cwd / man).write_text(text.replace("@PACKAGE_VERSION@", "4.2"))


def build(self):
    from cbuild.util import compiler

    cc = compiler.C(self)
    self.mkdir("obj", parents=True)
    objs = []
    for src in ["src/common.c", "src/charconv.c"]:
        obj = "obj/" + src.replace("/", "_").removesuffix(".c") + ".o"
        cc.invoke([src], obj, obj_file=True, flags=_cflags)
        objs.append(obj)
    self.do("ar", "rcs", "libcommon.a", *objs)

    cc.invoke(
        [
            "src/mkfs.fat.c",
            "src/device_info.c",
            "src/blkdev/blkdev.c",
            "src/blkdev/linux_version.c",
            "libcommon.a",
        ],
        "mkfs.fat",
        flags=_cflags,
    )
    cc.invoke(
        [
            "src/fsck.fat.c",
            "src/check.c",
            "src/file.c",
            "src/lfn.c",
            "src/boot.c",
            "src/fat.c",
            "src/io.c",
            "libcommon.a",
        ],
        "fsck.fat",
        flags=_cflags,
    )


def install(self):
    self.install_bin("mkfs.fat")
    self.install_bin("fsck.fat")
    self.install_man("fsck.fat.8")
    self.install_man("mkfs.fat.8")
    self.install_license("COPYING")
