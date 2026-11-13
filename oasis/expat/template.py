pkgname = "expat"
pkgver = "2.6.2"
pkgrel = 0
# Oasis pkg/expat/src
_commit = "fa75b96546c069d17b8f80d91e0f4ef0cde3790d"
pkgdesc = "XML parser library from Oasis"
license = "MIT"
url = "https://libexpat.github.io"
source = f"https://github.com/libexpat/libexpat/archive/{_commit}.tar.gz"
sha256 = "60764a53ad7bdc774df3619abbf2fc6754dbebb426616669be34b0faedc32155"
# no test suite
options = ["!check", "!lto"]

_sources = [
    "expat/lib/xmlparse.c",
    "expat/lib/xmltok.c",
    "expat/lib/xmlrole.c",
]


def pre_build(self):
    self.cp(self.files_path / "expat_config.h", "expat_config.h")


def build(self):
    from cbuild.util import compiler

    cc = compiler.C(self)
    objs = []
    flags = ["-std=c99", "-Wall", "-DHAVE_EXPAT_CONFIG_H", "-I."]
    self.mkdir("obj", parents=True)

    for src in _sources:
        obj = "obj/" + src.rsplit("/", 1)[-1].removesuffix(".c") + ".o"
        cc.invoke([src], obj, obj_file=True, flags=flags)
        objs.append(obj)

    self.do("ar", "rcs", "libexpat.a", *objs)


def install(self):
    self.install_file("libexpat.a", "usr/lib")
    self.install_file("expat/lib/expat.h", "usr/include")
    self.install_file("expat/lib/expat_external.h", "usr/include")
    self.install_license("COPYING")
