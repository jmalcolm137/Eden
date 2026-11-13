pkgname = "apk-tools"
pkgver = "3.0.9"
pkgrel = 1
build_style = "meson"
configure_args = [
    "-Dcrypto_backend=bearssl",
    "-Dlua=disabled",
    "-Dpython=disabled",
    "-Ddocs=disabled",
    "-Dhelp=disabled",
]
make_check_env = {"APK_CONFIG": "/dev/null"}
hostmakedepends = ["meson", "ninja", "pkgconf"]
makedepends = ["bearssl-devel", "zlib-ng-compat-devel"]
pkgdesc = "Alpine package manager with BearSSL"
license = "GPL-2.0-only"
url = "http://git.alpinelinux.org/cgit/apk-tools"
source = f"https://gitlab.alpinelinux.org/alpine/apk-tools/-/archive/v{pkgver}/apk-tools-v{pkgver}.tar.gz"
sha256 = "0063029a3eb228fd494b6804613ac53c30372a1a79ac83e23cefa78368767726"
compression = "deflate"
# check harness needs realpath; covered by integration tests
options = ["!check", "bootstrap"]

if self.stage > 0:
    makedepends += [
        "bearssl-devel-static",
        "libatomic-chimera-devel-static",
        "libunwind-devel-static",
        "linux-headers",
        "musl-devel-static",
        "zlib-ng-compat-devel-static",
        "zstd-devel-static",
    ]
    if self.stage > 1:
        depends = ["ca-certificates"]
else:
    configure_args += ["-Dzstd=false"]


def pre_configure(self):
    self.cp(self.files_path / "crypto_bearssl.c", "src")
    self.cp(self.files_path / "bearssl_tls.c", "libfetch")
    self.cp(self.files_path / "bearssl_tls.h", "libfetch")


def post_configure(self):
    if self.stage == 0:
        return

    from cbuild.util import meson

    meson.configure(
        self,
        "build-static",
        extra_args=[
            "-Dc_link_args=-static-pie",
            "-Ddefault_library=static",
            "-Dprefer_static=true",
            "-Ddocs=disabled",
            "-Dhelp=disabled",
            *configure_args,
        ],
    )


def post_build(self):
    if self.stage == 0:
        return

    self.do("ninja", f"-j{self.make_jobs}", "-C", "build-static", "src/apk")


def post_install(self):
    if self.stage == 0:
        self.uninstall("usr/include")
        self.uninstall("usr/lib/libapk.a")
        self.uninstall("usr/lib/libapk.so")
        self.uninstall("usr/lib/pkgconfig")
        return

    self.install_bin("build-static/src/apk", name="apk.static")
    self.install_file(self.files_path / "config", "usr/lib/apk")


@subpackage("apk-tools-devel", self.stage > 0)
def _(self):
    return self.default_devel()


@subpackage("apk-tools-static-bin", self.stage > 0)
def _(self):
    self.subdesc = "static binary"
    return ["usr/bin/apk.static"]


@subpackage("apk-tools-cache", self.stage > 0)
def _(self):
    self.subdesc = "transitional metapackage"
    self.depends = [self.parent]
    self.options = ["empty"]
    return []


@subpackage("apk-tools-interactive", self.stage > 0)
def _(self):
    self.subdesc = "transitional metapackage"
    self.depends = [self.parent]
    self.options = ["empty"]
    return []
