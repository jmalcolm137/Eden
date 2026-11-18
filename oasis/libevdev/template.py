pkgname = "libevdev"
pkgver = "1.12.0"
pkgrel = 1
# Oasis pkg/libevdev/src
_commit = "69403a63ed29a1ee62edb8d0885fa770dd9a53cf"
build_style = "meson"
configure_args = ["-Dtests=disabled", "-Ddocumentation=disabled"]
hostmakedepends = ["muon", "pkgconf", "python", "samurai"]
makedepends = [
    "libatomic-chimera-devel-static",
    "libunwind-devel-static",
    "linux-headers",
    "musl-devel-static",
]
pkgdesc = "Wrapper library for evdev devices"
license = "MIT"
url = "https://gitlab.freedesktop.org/libevdev/libevdev"
source = f"{url}/-/archive/{_commit}/libevdev-{_commit}.tar.gz"
sha256 = "c920f89f3c71807f625decae655f58be1d93a29cfdc729887b6ebb67a76c0f17"
# no test suite in the Oasis recipe
options = ["!check"]


def pre_configure(self):
    p = self.cwd / "meson_options.txt"
    p.write_text(p.read_text().replace("value: 'false'", "value: false"))


@subpackage("libevdev-devel")
def _(self):
    return self.default_devel()


def post_build(self):
    # Keep libevdev.so for libinput; link the bundled tools statically.
    from cbuild.util import compiler

    cc = compiler.C(self)
    for src, out in [
        ("tools/touchpad-edge-detector.c", "touchpad-edge-detector-static"),
        ("tools/mouse-dpi-tool.c", "mouse-dpi-tool-static"),
        ("tools/libevdev-tweak-device.c", "libevdev-tweak-device-static"),
    ]:
        cc.invoke(
            [src],
            out,
            flags=["-DHAVE_CONFIG_H", "-I.", "-Ilibevdev", "-Ibuild"],
            ldflags=["build/libevdev.a", "-lm", "-static-pie"],
        )


def post_install(self):
    self.install_license("COPYING")
    for name in [
        "touchpad-edge-detector",
        "mouse-dpi-tool",
        "libevdev-tweak-device",
    ]:
        self.uninstall(f"usr/bin/{name}", missing_ok=True)
        self.install_bin(f"{name}-static", name=name)
