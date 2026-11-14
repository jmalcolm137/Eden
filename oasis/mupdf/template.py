pkgname = "mupdf"
pkgver = "1.18.0"
pkgrel = 1
build_style = "makefile"
make_dir = "."
make_build_target = "build=release"
make_build_args = ["HAVE_X11=no", "HAVE_GLUT=no", "XCXXFLAGS=-Wno-error -Wno-unused-but-set-variable -Wno-cast-function-type-strict"]
make_use_env = True
pkgdesc = "Lightweight PDF and XPS viewer and tools"
license = "AGPL-3.0-or-later"
url = "https://mupdf.com"
source = "https://mupdf.com/downloads/archive/mupdf-1.18.0-source.tar.xz"
sha256 = "592d4f6c0fba41bb954eb1a41616661b62b134d5b383e33bd45a081af5d4a59a"
tool_flags = {"CFLAGS": ["-Wno-cast-function-type-strict"], "CXXFLAGS": ["-Wno-cast-function-type-strict"]}
# static-only libraries, as in the Oasis recipe
options = ["!lto", "!check"]


def init_build(self):
    self.make_build_env = {
        "CFLAGS": self.get_cflags(shell=True)
        + " -Iinclude -Wno-error -Wno-unused-but-set-variable -Wno-cast-function-type-strict"
    }


def pre_build(self):
    p = self.cwd / "Makefile"
    text = p.read_text()
    text = text.replace(
        "$(LD) -r -b binary -z noexecstack -o $@ $<",
        "$(OBJCOPY) -I binary -O elf64-x86-64 -B i386:x86-64 $< $@",
    )
    text = text.replace(
        "CFLAGS += $(XCFLAGS) -Iinclude",
        "override CFLAGS += $(XCFLAGS) -Iinclude -Wno-error -Wno-unused-but-set-variable -Wno-cast-function-type-strict",
    )
    p.write_text(text)
    p = self.cwd / "thirdparty/harfbuzz/src/hb-ft.cc"
    text = p.read_text()
    text = text.replace(
        '#include "hb-ft.h"',
        '#pragma clang diagnostic ignored "-Wcast-function-type-strict"\n#include "hb-ft.h"',
        1,
    )
    text = text.replace(
        "(FT_Generic_Finalizer) hb_ft_face_finalize",
        "(FT_Generic_Finalizer) (void (*)(void *)) hb_ft_face_finalize",
    )
    text = text.replace(
        "(FT_Generic_Finalizer) _release_blob",
        "(FT_Generic_Finalizer) (void (*)(void *)) _release_blob",
    )
    p.write_text(text)
    p = self.cwd / "thirdparty/harfbuzz/src/hb-subset-cff1.cc"
    text = p.read_text()
    text = text.replace(
        "unsigned int  size0, size1, supp_size;",
        "unsigned int  size0, size1, supp_size;\n    (void)supp_size;",
    )
    p.write_text(text)


def install(self):
    self.install_bin("build/release/mutool")
    self.install_bin("build/release/muraster")
    for lib in (
        "libmupdf.a",
        "libmupdf-pkcs7.a",
        "libmupdf-third.a",
        "libmupdf-threads.a",
    ):
        self.install_lib(f"build/release/{lib}", mode=0o644)
    self.install_files("include/mupdf", "usr/include", name="mupdf")
    self.install_man("docs/man/mutool.1")
    self.install_license("COPYING")


@subpackage("mupdf-devel")
def _(self):
    return ["usr/include"]
