pkgname = "libtermkey"
pkgver = "0.22"
pkgrel = 0
makedepends = ["netbsd-curses-devel"]
pkgdesc = "Terminal key input library"
license = "MIT"
url = "https://www.leonerd.org.uk/code/libtermkey"
source = f"{url}/libtermkey-{pkgver}.tar.gz"
sha256 = "6945bd3c4aaa83da83d80a045c5563da4edd7d0374c62c0d35aec09eb3014600"
tool_flags = {"CFLAGS": ["-fPIC"]}
# upstream tests need prove and a terminal
# static library is installed in the main package, like Oasis does
options = ["!check", "!lto"]

_sources = ["termkey.c", "driver-csi.c", "driver-ti.c"]


def build(self):
    from cbuild.util import compiler

    cc = compiler.C(self)
    objs = []

    for src in _sources:
        obj = src.removesuffix(".c") + ".o"
        cc.invoke([src], obj, obj_file=True)
        objs.append(obj)

    self.do("ar", "rcs", "libtermkey.a", *objs)


def install(self):
    self.install_file("libtermkey.a", "usr/lib")
    self.install_file("termkey.h", "usr/include")
    self.install_file(self.files_path / "termkey.pc", "usr/lib/pkgconfig")
    self.install_license("LICENSE")
