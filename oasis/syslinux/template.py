pkgname = "syslinux"
pkgver = "6.03"
pkgrel = 0
makedepends = ["linux-headers"]
pkgdesc = "Bootloader suite"
license = "GPL-2.0-or-later"
url = "https://www.syslinux.org"
source = "https://www.kernel.org/pub/linux/utils/boot/syslinux/syslinux-6.03.tar.xz"
sha256 = "26d3986d2bea109d5dc0e4f8c4822a459276cf021125e8c9f23c3cca5d8c850e"
# only the extlinux installer and MBR are built, as in the Oasis recipe
options = ["!check"]

_cflags = [
    "-Wall", "-Wno-address-of-packed-member",
    "-I.", "-Ilibinstaller", "-Icom32/include/syslinux",
]


def pre_build(self):
    self.cp(self.files_path / "bin2c.c", self.cwd / "bin2c.c")
    self.cp(self.files_path / "version.awk", self.cwd / "version.awk")
    self.mkdir("uuid", parents=True)
    self.cp(self.files_path / "uuid" / "uuid.h", self.cwd / "uuid" / "uuid.h")


def build(self):
    from cbuild.util import compiler

    cc = compiler.C(self)
    cc.invoke(
        ["bin2c.c"], "bin2c",
        flags=["-std=c99", "-Wall", "-Wextra", "-Wpedantic"],
    )
    with open(self.cwd / "version.h", "w") as f:
        self.do(
            "awk", "-f", "version.awk", "-v", "fmt=#define %s %s",
            "version", stdout=f,
        )
    for src, args in [
        ("bios/core/ldlinux.bss", ["syslinux_bootsect"]),
        ("bios/core/ldlinux.sys", ["syslinux_ldlinux", "512"]),
        ("bios/com32/elflink/ldlinux/ldlinux.c32", ["syslinux_ldlinuxc32"]),
    ]:
        name = args[0]
        with open(self.cwd / f"{name}.c", "w") as f:
            self.do("./bin2c", *args, input=(self.cwd / src).read_bytes(), stdout=f)
    srcs = [
        "extlinux/main.c", "extlinux/mountinfo.c",
        "libinstaller/syslxmod.c", "libinstaller/syslxopt.c",
        "libinstaller/syslxcom.c", "libinstaller/setadv.c",
        "libinstaller/advio.c",
        "syslinux_bootsect.c", "syslinux_ldlinux.c", "syslinux_ldlinuxc32.c",
    ]
    cc.invoke(srcs, "extlinux-bin", flags=_cflags)


def install(self):
    self.install_bin("extlinux-bin", name="extlinux")
    self.install_file("bios/mbr/mbr.bin", "usr/lib/syslinux/bios", mode=0o644)
    self.install_license("COPYING")
