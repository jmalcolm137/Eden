pkgname = "musl-obstack"
pkgver = "1.2.3"
pkgrel = 0
pkgdesc = "Implementation of obstack for musl"
license = "GPL-2.0-or-later"
url = "https://github.com/void-linux/musl-obstack"
source = f"{url}/archive/v{pkgver}.tar.gz"
sha256 = "9ffb3479b15df0170eba4480e51723c3961dbe0b461ec289744622db03a69395"
# no test suite
options = ["!check", "!lto"]


def pre_build(self):
    (self.cwd / "config.h").write_text(
        "#define HAVE_LIBINTL_H 0\n#define ENABLE_NLS 0\n"
    )


def build(self):
    from cbuild.util import compiler

    cc = compiler.C(self)
    objs = []
    for src in ["obstack.c", "obstack_printf.c"]:
        obj = src.removesuffix(".c") + ".o"
        cc.invoke([src], obj, obj_file=True, flags=["-I."])
        objs.append(obj)
    self.do("ar", "rcs", "libobstack.a", *objs)


def install(self):
    self.install_file("libobstack.a", "usr/lib")
    self.install_file("obstack.h", "usr/include")
    self.install_license("COPYING")
