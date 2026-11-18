pkgname = "xz"
pkgver = "5.8.4"
pkgrel = 3
build_style = "gnu_configure"
configure_args = ["--disable-nls", "--disable-sandbox"]
configure_gen = []
make_build_env = {
    "ACLOCAL": "true",
    "AUTOCONF": "true",
    "AUTOHEADER": "true",
    "AUTOMAKE": "true",
    "MAKEINFO": "true",
}
hostmakedepends = ["pkgconf"]
makedepends = [
    "libatomic-chimera-devel-static",
    "musl-devel-static",
]
renames = ["liblzma"]
pkgdesc = "XZ compression utilities"
license = "0BSD"
url = "https://tukaani.org/xz"
source = f"https://github.com/tukaani-project/xz/releases/download/v{pkgver}/xz-{pkgver}.tar.gz"
sha256 = "0014c7886930454fe8bd4228665b51af55eeae560ea135c9c4cd33f55b2591d9"
options = ["bootstrap"]


if self.stage > 0:
    makedepends += ["linux-headers"]


def pre_configure(self):
    # We use the pre-generated autotools files; keep make from trying to
    # regenerate them after the patches touch configure.ac/Makefile.am.
    for f in list(self.cwd.rglob("Makefile.in")):
        f.touch()
    for f in ("aclocal.m4", "configure", "config.h.in"):
        p = self.cwd / f
        if p.exists():
            p.touch()


def post_build(self):
    # Keep liblzma.so for consumers and relink the command line tools
    # against the static archive.
    from cbuild.util import compiler

    cc = compiler.C(self)
    libs = [
        "build/src/liblzma/.libs/liblzma.a",
        "-lpthread",
        "-lm",
        "-static-pie",
        "-unwindlib=none",
    ]
    xz_objs = [
        str(p.relative_to(self.cwd))
        for p in sorted((self.cwd / "build/src/xz").glob("*.o"))
    ]
    cc.invoke(xz_objs, "xz-static", ldflags=libs)
    for prefix, out in [("xzdec", "xzdec-static"), ("lzmadec", "lzmadec-static")]:
        objs = [
            str(p.relative_to(self.cwd))
            for p in sorted((self.cwd / "build/src/xzdec").glob(prefix + "-*.o"))
        ]
        cc.invoke(objs, out, ldflags=libs)
    objs = [
        str(p.relative_to(self.cwd))
        for p in sorted((self.cwd / "build/src/lzmainfo").glob("lzmainfo-*.o"))
    ]
    cc.invoke(objs, "lzmainfo-static", ldflags=libs)


def post_install(self):
    self.install_license("COPYING")
    for name in ["xz", "xzdec", "lzmadec", "lzmainfo"]:
        self.uninstall(f"usr/bin/{name}", missing_ok=True)
        self.install_bin(f"{name}-static", name=name)
    self.uninstall("usr/share/doc")
    for tool in [
        "xzgrep",
        "xzfgrep",
        "xzegrep",
        "lzgrep",
        "lzfgrep",
        "lzegrep",
        "xzdiff",
        "lzdiff",
        "xzcmp",
        "lzcmp",
        "xzless",
        "xzmore",
        "lzless",
        "lzmore",
    ]:
        self.uninstall(f"usr/bin/{tool}")
        self.uninstall(f"usr/share/man/man1/{tool + '.1'}")


@subpackage("xz-devel")
def _(self):
    self.renames = ["liblzma-devel"]

    return self.default_devel()
