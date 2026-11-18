pkgname = "fontconfig"
pkgver = "2.18.3"
pkgrel = 2
build_style = "gnu_configure"
configure_args = [
    "--disable-docs",
    "--enable-static",
    "--with-cache-dir=/var/cache/fontconfig",
]
configure_gen = []
hostmakedepends = [
    "gettext",
    "gperf",
    "pkgconf",
    "python",
]
makedepends = [
    "freetype-devel",
    "freetype-devel-static",
    "libatomic-chimera-devel-static",
    "libexpat-devel",
    "libexpat-devel-static",
    "libunwind-devel-static",
    "musl-devel-static",
]
triggers = ["/usr/share/fonts/*"]
pkgdesc = "Library for configuring and customizing font access"
license = "MIT"
url = "https://www.fontconfig.org"
source = "https://gitlab.freedesktop.org/api/v4/projects/890/packages/generic/fontconfig/2.18.3/fontconfig-2.18.3.tar.xz"
sha256 = "4f7b554a38cdf78c033f666c8871f3749e14a094f65a07f630c91ed0b43d35e3"
# tests require a display and test fonts
options = ["etcfiles", "!check", "!splitstatic"]


def post_build(self):
    # Keep libfontconfig.so for consumers and relink the fc-* tools against
    # the static archive.
    from cbuild.util import compiler

    cc = compiler.C(self)
    libs = [
        "build/src/.libs/libfontconfig.a",
        "-lfreetype",
        "-lexpat",
        "-lz",
        "-lm",
        "-lpthread",
        "-static-pie",
    ]
    for name in [
        "fc-cache",
        "fc-cat",
        "fc-conflist",
        "fc-list",
        "fc-match",
        "fc-pattern",
        "fc-query",
        "fc-scan",
        "fc-validate",
    ]:
        cc.invoke(
            [f"build/{name}/{name}.o"], f"{name}-static", ldflags=libs
        )


def post_install(self):
    for name in [
        "fc-cache",
        "fc-cat",
        "fc-conflist",
        "fc-list",
        "fc-match",
        "fc-pattern",
        "fc-query",
        "fc-scan",
        "fc-validate",
    ]:
        self.uninstall(f"usr/bin/{name}", missing_ok=True)
        self.install_bin(f"{name}-static", name=name)
    self.install_license("COPYING")


@subpackage("fontconfig-devel")
def _(self):
    return self.default_devel()
