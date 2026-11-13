pkgname = "nasm"
pkgver = "2.16.01"
pkgrel = 0
# Oasis pkg/nasm
pkgdesc = "80x86 assembler designed for portability and modularity"
license = "BSD-2-Clause"
url = "https://www.nasm.us"
source = f"{url}/pub/nasm/releasebuilds/{pkgver}/nasm-{pkgver}.tar.gz"
sha256 = "d833bf0f5716e89dbcd345b7f545f25fe348c6e2ef16dbc293e1027bcd22d881"
# no test suite in the bootstrap environment
options = ["!check"]

_lib_sources = [
    "stdlib/snprintf.c",
    "stdlib/vsnprintf.c",
    "stdlib/strlcpy.c",
    "stdlib/strnlen.c",
    "stdlib/strrchrnul.c",
    "nasmlib/ver.c",
    "nasmlib/alloc.c",
    "nasmlib/asprintf.c",
    "nasmlib/errfile.c",
    "nasmlib/crc32.c",
    "nasmlib/crc64.c",
    "nasmlib/md5c.c",
    "nasmlib/string.c",
    "nasmlib/nctype.c",
    "nasmlib/file.c",
    "nasmlib/mmap.c",
    "nasmlib/ilog2.c",
    "nasmlib/realpath.c",
    "nasmlib/path.c",
    "nasmlib/filename.c",
    "nasmlib/rlimit.c",
    "nasmlib/zerobuf.c",
    "nasmlib/readnum.c",
    "nasmlib/bsi.c",
    "nasmlib/rbtree.c",
    "nasmlib/hashtbl.c",
    "nasmlib/raa.c",
    "nasmlib/saa.c",
    "nasmlib/strlist.c",
    "nasmlib/perfhash.c",
    "nasmlib/badenum.c",
    "common/common.c",
    "x86/insnsa.c",
    "x86/insnsb.c",
    "x86/insnsd.c",
    "x86/insnsn.c",
    "x86/regs.c",
    "x86/regvals.c",
    "x86/regflags.c",
    "x86/regdis.c",
    "x86/disp8.c",
    "x86/iflag.c",
    "asm/error.c",
    "asm/warnings.c",
    "asm/floats.c",
    "asm/directiv.c",
    "asm/directbl.c",
    "asm/pragma.c",
    "asm/assemble.c",
    "asm/labels.c",
    "asm/parser.c",
    "asm/preproc.c",
    "asm/quote.c",
    "asm/pptok.c",
    "asm/listing.c",
    "asm/eval.c",
    "asm/exprlib.c",
    "asm/exprdump.c",
    "asm/stdscan.c",
    "asm/strfunc.c",
    "asm/tokhash.c",
    "asm/segalloc.c",
    "asm/rdstrnum.c",
    "asm/srcfile.c",
    "macros/macros.c",
    "output/outform.c",
    "output/outlib.c",
    "output/legacy.c",
    "output/nulldbg.c",
    "output/nullout.c",
    "output/outbin.c",
    "output/outaout.c",
    "output/outcoff.c",
    "output/outelf.c",
    "output/outobj.c",
    "output/outas86.c",
    "output/outdbg.c",
    "output/outieee.c",
    "output/outmacho.c",
    "output/codeview.c",
    "disasm/disasm.c",
    "disasm/sync.c",
]


def pre_build(self):
    self.mkdir("config", parents=True)
    self.cp(self.files_path / "config.h", "config/config.h")


def build(self):
    from cbuild.util import compiler

    cc = compiler.C(self)
    flags = [
        "-DHAVE_CONFIG_H",
        "-DHAVE___BUILTIN_CHOOSE_EXPR=1",
        "-DHAVE___BUILTIN_CLZ=1",
        "-I.",
        "-Iinclude",
        "-Ix86",
        "-Iasm",
        "-Idisasm",
        "-Ioutput",
    ]
    self.mkdir("obj", parents=True)

    objs = []
    for src in _lib_sources:
        obj = "obj/" + src.replace("/", "_").removesuffix(".c") + ".o"
        cc.invoke([src], obj, obj_file=True, flags=flags)
        objs.append(obj)
    self.do("ar", "rcs", "libnasm.a", *objs)

    cc.invoke(["asm/nasm.c"], "obj/nasm-main.o", obj_file=True, flags=flags)
    cc.invoke(["obj/nasm-main.o", "libnasm.a"], "nasm")


def install(self):
    self.install_bin("nasm")
    self.install_man("nasm.1")
    self.install_license("LICENSE")
