pkgname = "f2fs-tools"
pkgver = "1.14.0"
pkgrel = 2
# Oasis pkg/f2fs-tools/src
_commit = "d41dcbdf46dc3841cd0a0507e6573e38cb6c55bb"
makedepends = ["linux-headers", "e2fsprogs-devel", "e2fsprogs-devel-static"]
pkgdesc = "Tools for the F2FS filesystem"
license = "GPL-2.0-or-later"
url = "https://git.kernel.org/pub/scm/linux/kernel/git/jaegeuk/f2fs-tools.git"
source = f"{url}/snapshot/f2fs-tools-{_commit}.tar.gz"
sha256 = "e54b6f44d2ad68d2c9da6b8f342161fad4c9d5fdc1e266a18145f862e736ea94"
# no test suite in the Oasis recipe
options = ["!check"]

_cflags = [
    "-Wall",
    "-Wno-address-of-packed-member",
    "-DHAVE_CONFIG_H",
    "-I.",
    "-Iinclude",
    "-I/usr/include/uuid",
]


def pre_build(self):
    self.cp(self.files_path / "config.h", "config.h")


def build(self):
    from cbuild.util import compiler

    cc = compiler.C(self)
    self.mkdir("obj", parents=True)
    objs = []
    for src in [
        "libf2fs.c",
        "libf2fs_io.c",
        "libf2fs_zoned.c",
        "nls_utf8.c",
    ]:
        obj = "obj/" + src.removesuffix(".c") + ".o"
        cc.invoke([f"lib/{src}"], obj, obj_file=True, flags=_cflags)
        objs.append(obj)
    self.do("ar", "rcs", "libf2fs.a", *objs)

    cc.invoke(
        [
            "mkfs/f2fs_format_main.c",
            "mkfs/f2fs_format.c",
            "mkfs/f2fs_format_utils.c",
            "libf2fs.a",
        ],
        "mkfs.f2fs",
        flags=_cflags,
        ldflags=["/usr/lib/libuuid.so"],
    )
    cc.invoke(
        [
            "fsck/main.c",
            "fsck/fsck.c",
            "fsck/dump.c",
            "fsck/mount.c",
            "fsck/defrag.c",
            "fsck/resize.c",
            "fsck/node.c",
            "fsck/segment.c",
            "fsck/dir.c",
            "fsck/sload.c",
            "fsck/xattr.c",
            "fsck/dict.c",
            "fsck/mkquota.c",
            "fsck/quotaio.c",
            "fsck/quotaio_tree.c",
            "fsck/quotaio_v2.c",
            "libf2fs.a",
        ],
        "fsck.f2fs",
        flags=_cflags,
    )


def install(self):
    self.install_bin("mkfs.f2fs")
    self.install_bin("fsck.f2fs")
    self.install_man("man/mkfs.f2fs.8")
    self.install_man("man/fsck.f2fs.8")
    self.install_license("COPYING")
