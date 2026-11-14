pkgname = "efivar"
pkgver = "39"
pkgrel = 0
# Oasis pkg/efivar/src
_commit = "c47820c37ac26286559ec004de07d48d05f3308c"
makedepends = ["linux-headers"]
pkgdesc = "Tools and library for manipulating EFI variables"
license = "LGPL-2.1-or-later"
url = "https://github.com/rhinstaller/efivar"
source = f"{url}/archive/{_commit}.tar.gz"
sha256 = "0fb98e5c0dd6d428bdc68fe6ac9cd2f939c2a140bdf38179bb1f4f990ac9a9d0"
# static-only library, as in the Oasis recipe
options = ["!lto", "!check"]

_cflags = [
    "-Wall",
    "-Wextra",
    "-D_GNU_SOURCE",
    "-DLIBEFIVAR_VERSION=39",
    "-include",
    "compat.h",
    "-I.",
    "-Isrc",
    "-Isrc/include",
    "-Iobj/include",
]

_boot_sources = [
    "src/creator.c",
    "src/disk.c",
    "src/gpt.c",
    "src/loadopt.c",
    "src/path-helpers.c",
    "src/linux.c",
    "src/linux-acpi.c",
    "src/linux-acpi-root.c",
    "src/linux-ata.c",
    "src/linux-emmc.c",
    "src/linux-i2o.c",
    "src/linux-md.c",
    "src/linux-nvme.c",
    "src/linux-pci.c",
    "src/linux-pci-root.c",
    "src/linux-pmem.c",
    "src/linux-sas.c",
    "src/linux-sata.c",
    "src/linux-scsi.c",
    "src/linux-soc-root.c",
    "src/linux-virtblk.c",
    "src/linux-virtual-root.c",
]

_var_sources = [
    "src/dp.c",
    "src/dp-acpi.c",
    "src/dp-hw.c",
    "src/dp-media.c",
    "src/dp-message.c",
    "src/efivarfs.c",
    "src/error.c",
    "src/export.c",
    "src/guid.c",
    "src/lib.c",
    "src/vars.c",
    "src/time.c",
]

_headers = [
    "efiboot.h",
    "efiboot-creator.h",
    "efiboot-loadopt.h",
    "efivar.h",
    "efivar-dp.h",
    "efivar-time.h",
    "efivar-types.h",
]


def pre_build(self):
    self.cp(self.files_path / "compat.h", "compat.h")
    self.mkdir("obj/include/efivar", parents=True)
    self.mkdir("obj", parents=True)


def build(self):
    from cbuild.util import compiler

    cc = compiler.C(self)
    cc.invoke(
        ["src/makeguids.c", "src/util.c"],
        "makeguids",
        flags=["-DEFIVAR_BUILD_ENVIRONMENT", "-D_GNU_SOURCE", "-Isrc/include"],
    )
    self.do(
        "./makeguids",
        "src/guids.txt",
        "guid-symbols.c",
        "obj/include/efivar/efivar-guids.h",
    )

    objs = []
    for src in ["src/crc32.c"] + _boot_sources:
        obj = "obj/boot_" + src.replace("/", "_").removesuffix(".c") + ".o"
        cc.invoke([src], obj, obj_file=True, flags=_cflags)
        objs.append(obj)
    self.do("ar", "rcs", "libefiboot.a", *objs)

    objs = []
    for src in ["src/crc32.c"] + _var_sources + ["guid-symbols.c"]:
        obj = "obj/var_" + src.replace("/", "_").removesuffix(".c") + ".o"
        cc.invoke([src], obj, obj_file=True, flags=_cflags)
        objs.append(obj)
    self.do("ar", "rcs", "libefivar.a", *objs)


def install(self):
    self.install_lib("libefiboot.a", mode=0o644)
    self.install_lib("libefivar.a", mode=0o644)
    for h in _headers:
        self.install_file(f"src/include/efivar/{h}", "usr/include/efivar")
    self.install_file("obj/include/efivar/efivar-guids.h", "usr/include/efivar")
    self.install_license("COPYING")


@subpackage("efivar-devel")
def _(self):
    self.depends = [self.parent]
    return ["usr/include"]
