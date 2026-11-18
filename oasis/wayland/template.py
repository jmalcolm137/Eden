pkgname = "wayland"
pkgver = "1.26.0"
pkgrel = 1
build_style = "meson"
configure_args = [
    "-Ddocumentation=false",
    "-Ddtd_validation=false",
    "-Dtests=false",
]
hostmakedepends = [
    "muon",
    "pkgconf",
    "python",
    "samurai",
]
makedepends = [
    "libatomic-chimera-devel-static",
    "libexpat-devel",
    "libexpat-devel-static",
    "libffi8-devel",
    "libunwind-devel-static",
    "musl-devel-static",
]
pkgdesc = "Wayland display server protocol libraries"
license = "MIT"
url = "https://wayland.freedesktop.org"
source = "https://gitlab.freedesktop.org/wayland/wayland/-/archive/1.26.0/wayland-1.26.0.tar.gz"
sha256 = "56b3a985cbfe17a926e3bcf037e4d374f44eaa33f3a4b364549dddf0d324cebc"
# tests require a display or a full graphics stack
options = ["!check", "!splitstatic"]


@subpackage("wayland-devel")
def _(self):
    return self.default_devel()


@subpackage("wayland-progs")
def _(self):
    self.subdesc = "scanner and utilities"
    return ["usr/bin/wayland-scanner"]


def post_build(self):
    # meson links the utility and private objects into the shared libraries
    # but does not install them, so fold them into the static archives to
    # make static linking work like the previous Oasis build did
    objs = []
    for name in ("libwayland-util.a.p", "libwayland-private.a.p"):
        objs += [
            str(p.relative_to(self.cwd))
            for p in sorted((self.cwd / "build/src" / name).rglob("*.o"))
        ]
    for lib in ("wayland-client", "wayland-server"):
        self.do("ar", "rs", f"build/src/lib{lib}.a", *objs)

    # Relink wayland-scanner statically; the generated scanner is a host
    # tool and does not need the shared libraries.
    from cbuild.util import compiler

    cc = compiler.C(self)
    cc.invoke(
        ["src/scanner.c", "src/wayland-util.c"],
        "wayland-scanner-static",
        flags=["-DHAVE_CONFIG_H", "-I.", "-Iinclude", "-Isrc", "-Ibuild", "-Ibuild/src"],
        ldflags=["-static-pie", "-lexpat"],
    )


def post_install(self):
    self.install_license("COPYING")
    self.uninstall("usr/bin/wayland-scanner")
    self.install_bin("wayland-scanner-static", name="wayland-scanner")
