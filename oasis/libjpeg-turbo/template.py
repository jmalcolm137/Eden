pkgname = "libjpeg-turbo"
pkgver = "2.0.6"
pkgrel = 0
# Oasis pkg/libjpeg-turbo/src
_commit = "10ba6ed3365615ed5c2995fe2d240cb2d5000173"
pkgdesc = "JPEG image codec from Oasis"
license = "IJG AND BSD-3-Clause AND Zlib"
url = "https://libjpeg-turbo.org"
source = f"https://github.com/libjpeg-turbo/libjpeg-turbo/archive/{_commit}.tar.gz"
sha256 = "87fcfc2c107294a6a1fa0245ee09d0bd7e978e6a8652d0b3b53c40fd83cc28c0"
# no test suite
options = ["!check", "!lto"]

_sources = [
    "jcapimin.c", "jcapistd.c", "jccoefct.c", "jccolor.c", "jcdctmgr.c",
    "jchuff.c", "jcicc.c", "jcinit.c", "jcmainct.c", "jcmarker.c",
    "jcmaster.c", "jcomapi.c", "jcparam.c", "jcphuff.c", "jcprepct.c",
    "jcsample.c", "jctrans.c", "jdapimin.c", "jdapistd.c", "jdatadst.c",
    "jdatasrc.c", "jdcoefct.c", "jdcolor.c", "jddctmgr.c", "jdhuff.c",
    "jdicc.c", "jdinput.c", "jdmainct.c", "jdmarker.c", "jdmaster.c",
    "jdmerge.c", "jdphuff.c", "jdpostct.c", "jdsample.c", "jdtrans.c",
    "jerror.c", "jfdctflt.c", "jfdctfst.c", "jfdctint.c", "jidctflt.c",
    "jidctfst.c", "jidctint.c", "jidctred.c", "jquant1.c", "jquant2.c",
    "jutils.c", "jmemmgr.c", "jmemnobs.c", "jaricom.c", "jcarith.c",
    "jdarith.c", "jsimd_none.c",
]


def pre_build(self):
    self.cp(self.files_path / "jconfig.h", "jconfig.h")
    self.cp(self.files_path / "jconfigint.h", "jconfigint.h")


def build(self):
    from cbuild.util import compiler

    cc = compiler.C(self)
    objs = []
    flags = [
        "-I.",
        "-fPIC",
        "-DHAVE__THREAD_LOCAL=1",
        "-DHAVE___BUILTIN_CTZL=1",
    ]
    self.mkdir("obj", parents=True)

    for src in _sources:
        obj = "obj/" + src.removesuffix(".c") + ".o"
        cc.invoke([src], obj, obj_file=True, flags=flags)
        objs.append(obj)

    self.do("ar", "rcs", "libjpeg-turbo.a", *objs)
    vmap = self.cwd / "libjpeg8.map"
    vmap.write_text("LIBJPEG_8.0 {\n    global: *;\n};\n")
    self.do(
        self.get_tool("CC"),
        "-shared",
        "-fPIC",
        "-Wl,-soname,libjpeg.so.8",
        "-Wl,--version-script,libjpeg8.map",
        "-o",
        "libjpeg.so.8",
        *objs,
    )


def install(self):
    self.install_file("libjpeg-turbo.a", "usr/lib")
    self.install_file("libjpeg.so.8", "usr/lib")
    self.install_link("usr/lib/libjpeg.so", "libjpeg.so.8")
    self.install_file("jpeglib.h", "usr/include")
    self.install_file("jmorecfg.h", "usr/include")
    self.install_file("jconfig.h", "usr/include")
    self.install_file("jerror.h", "usr/include")

    pc = self.destdir / "usr/lib/pkgconfig/libjpeg.pc"
    pc.parent.mkdir(parents=True, exist_ok=True)
    pc.write_text(
        "prefix=/usr\n"
        "exec_prefix=${prefix}\n"
        "libdir=${exec_prefix}/lib\n"
        "includedir=${prefix}/include\n"
        "\n"
        "Name: libjpeg\n"
        "Description: JPEG image codec\n"
        "Version: 2.0.6\n"
        "Libs: -L${libdir} -ljpeg\n"
        "Cflags: -I${includedir}\n"
    )
    self.install_license("LICENSE.md")


@subpackage("libjpeg-turbo-devel")
def _(self):
    # the static build keeps headers in the main package for Oasis consumers
    self.depends = [self.parent]
    self.options = ["empty"]
    return []
