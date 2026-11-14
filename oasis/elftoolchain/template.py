pkgname = "elftoolchain"
pkgver = "0_git20200101"
pkgrel = 1
# Oasis pkg/elftoolchain/src
_commit = "f7e9afc6f9ad0d84ea73b4659c5d6d13275d2306"
makedepends = ["m4", "musl-bsd-headers"]
pkgdesc = "ELF object file access library"
license = "BSD-2-Clause"
url = "https://github.com/elftoolchain/elftoolchain"
source = f"{url}/archive/{_commit}.tar.gz"
sha256 = "3d9e0513af4b7cb8ac7944d98057b8d61fcc4ff326b030a7b06006c0abb7922c"
# static-only library, as in the Oasis recipe
options = ["!lto", "!check"]

_cflags = ["-Wall", "-Wpedantic", "-I.", "-Icommon", "-Ilibelf", "-Iobj/include"]

_sources = [
    "libelf/elf.c", "libelf/elf_begin.c", "libelf/elf_cntl.c", "libelf/elf_end.c",
    "libelf/elf_errmsg.c", "libelf/elf_errno.c", "libelf/elf_data.c",
    "libelf/elf_fill.c", "libelf/elf_flag.c", "libelf/elf_getarhdr.c",
    "libelf/elf_getarsym.c", "libelf/elf_getbase.c", "libelf/elf_getident.c",
    "libelf/elf_getversion.c", "libelf/elf_hash.c", "libelf/elf_kind.c",
    "libelf/elf_memory.c", "libelf/elf_next.c", "libelf/elf_open.c",
    "libelf/elf_rand.c", "libelf/elf_rawfile.c", "libelf/elf_phnum.c",
    "libelf/elf_shnum.c", "libelf/elf_shstrndx.c", "libelf/elf_scn.c",
    "libelf/elf_strptr.c", "libelf/elf_update.c", "libelf/elf_version.c",
    "libelf/gelf_cap.c", "libelf/gelf_checksum.c", "libelf/gelf_dyn.c",
    "libelf/gelf_ehdr.c", "libelf/gelf_getclass.c", "libelf/gelf_fsize.c",
    "libelf/gelf_move.c", "libelf/gelf_phdr.c", "libelf/gelf_rel.c",
    "libelf/gelf_rela.c", "libelf/gelf_shdr.c", "libelf/gelf_sym.c",
    "libelf/gelf_syminfo.c", "libelf/gelf_symshndx.c", "libelf/gelf_xlate.c",
    "libelf/libelf_align.c", "libelf/libelf_allocate.c", "libelf/libelf_ar.c",
    "libelf/libelf_ar_util.c", "libelf/libelf_checksum.c", "libelf/libelf_data.c",
    "libelf/libelf_ehdr.c", "libelf/libelf_elfmachine.c", "libelf/libelf_extended.c",
    "libelf/libelf_memory.c", "libelf/libelf_open.c", "libelf/libelf_phdr.c",
    "libelf/libelf_shdr.c", "libelf/libelf_xlate.c",
]


def pre_build(self):
    self.mkdir("obj/include/sys", parents=True)
    self.do(
        "sh", "-c",
        "m4 -D SRCDIR=libelf libelf/libelf_convert.m4 > obj/libelf_convert.c",
    )
    self.do(
        "sh", "-c",
        "m4 -D SRCDIR=libelf libelf/libelf_fsize.m4 > obj/libelf_fsize.c",
    )
    self.do(
        "sh", "-c",
        "m4 -D SRCDIR=libelf libelf/libelf_msize.m4 > obj/libelf_msize.c",
    )
    self.do(
        "sh", "-c",
        "m4 -I common/sys common/sys/elfdefinitions.m4 > obj/include/sys/elfdefinitions.h",
    )


def build(self):
    from cbuild.util import compiler

    cc = compiler.C(self)
    self.mkdir("obj", parents=True)
    objs = []
    for src in _sources + [
        "obj/libelf_convert.c", "obj/libelf_fsize.c", "obj/libelf_msize.c",
    ]:
        obj = "obj/" + src.replace("/", "_").removesuffix(".c") + ".o"
        cc.invoke([src], obj, obj_file=True, flags=_cflags)
        objs.append(obj)
    self.do("ar", "rcs", "libelf.a", *objs)


def install(self):
    self.install_lib("libelf.a", mode=0o644)
    self.install_file("libelf/libelf.h", "usr/include")
    self.install_file("libelf/gelf.h", "usr/include")
    self.install_file("common/elfdefinitions.h", "usr/include")
    self.install_file("obj/include/sys/elfdefinitions.h", "usr/include/sys")
    self.install_license("LICENSE")


@subpackage("elftoolchain-devel")
def _(self):
    return ["usr/include"]
