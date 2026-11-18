pkgname = "pixman"
pkgver = "0.46.4"
pkgrel = 0
build_style = "meson"
configure_args = [
    "-Ddemos=disabled",
    "-Dgnu-inline-asm=enabled",
    "-Dgtk=disabled",
    "-Dlibpng=disabled",
    "-Dopenmp=disabled",
    "-Dtests=disabled",
]
hostmakedepends = [
    "muon",
    "perl",
    "pkgconf",
    "samurai",
]
makedepends = [
    "linux-headers",
]
pkgdesc = "Pixel manipulation library"
license = "MIT"
url = "https://pixman.org"
source = "https://www.cairographics.org/releases/pixman-0.46.4.tar.gz"
sha256 = "d09c44ebc3bd5bee7021c79f922fe8fb2fb57f7320f55e97ff9914d2346a591c"
# tests require a display or a full graphics stack
options = ["!check", "!splitstatic"]


@subpackage("pixman-devel")
def _(self):
    return self.default_devel()


def post_build(self):
    # meson links the SIMD objects into the shared library but does not
    # install them, so fold them into the static archive for static linking
    objs = []
    for d in (self.cwd / "build/pixman").glob("libpixman-*.a.p"):
        if d.name == "libpixman-1.a.p":
            continue
        objs += [
            str(p.relative_to(self.cwd)) for p in sorted(d.rglob("*.o"))
        ]
    self.do("ar", "rs", "build/pixman/libpixman-1.a", *objs)


def post_install(self):
    self.install_license("COPYING")
