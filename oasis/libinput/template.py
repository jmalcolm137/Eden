pkgname = "libinput"
pkgver = "1.31.3"
pkgrel = 2
build_style = "meson"
configure_args = [
    "-Dautoload-plugins=false",
    "-Ddebug-gui=false",
    "-Ddefault_library=both",
    "-Ddocumentation=false",
    "-Dinstall-tests=false",
    "-Dinternal-event-debugging=false",
    "-Dlibwacom=false",
    "-Dlua-plugins=disabled",
    "-Dmtdev=true",
    "-Dtests=false",
]
hostmakedepends = [
    "muon",
    "pkgconf",
    "samurai",
]
makedepends = [
    "libatomic-chimera-devel-static",
    "libevdev-devel",
    "libevdev-devel-static",
    "libunwind-devel-static",
    "linux-headers",
    "mtdev-devel",
    "musl-devel-static",
    "udev-devel",
    "udev-devel-static",
]
pkgdesc = "Input device handling library"
license = "MIT"
url = "https://www.freedesktop.org/wiki/Software/libinput"
source = "https://gitlab.freedesktop.org/libinput/libinput/-/archive/1.31.3/libinput-1.31.3.tar.gz"
sha256 = "b6749bf6f1890f6631c0a70a027c35fec9d2e096a39f720548896e41474a9854"
# tests require a display or a full graphics stack
options = ["!check"]


@subpackage("libinput-devel")
def _(self):
    return self.default_devel()


def post_patch(self):
    # upstream hardcodes shared_library; build both so the Oasis stack can
    # consume a static libinput
    p = self.cwd / "meson.build"
    s = p.read_text()
    s = s.replace(
        "lib_libinput = shared_library('input',",
        "lib_libinput = library('input',",
    )
    p.write_text(s)


def post_build(self):
    # Keep the shared libinput for consumers and link the CLI statically.
    from cbuild.util import compiler

    cc = compiler.C(self)
    cc.invoke(
        ["build/libinput.p/tools/libinput-tool.c.o"],
        "libinput-static",
        ldflags=[
            "build/libtools_shared.a",
            "build/libinput.a",
            "build/liblibinput-util.a",
            "build/liblibinput-util-libinput.a",
            "build/libfilter.a",
            "build/libquirks.a",
            "-levdev",
            "-lmtdev",
            "-ludev",
            "-lm",
            "-lpthread",
            "-static-pie",
        ],
    )


def post_install(self):
    # ship the internal static archives that the shared libinput links in,
    # so static consumers can resolve list/strv/quirks/filter symbols
    for f in (
        "libfilter.a",
        "libquirks.a",
        "liblibinput-util.a",
        "liblibinput-util-libinput.a",
    ):
        self.install_file(f"build/{f}", "usr/lib", mode=0o644)
    self.uninstall("usr/bin/libinput", missing_ok=True)
    self.install_bin("libinput-static", name="libinput")
    self.install_license("COPYING")
