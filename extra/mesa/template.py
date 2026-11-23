pkgname = "mesa"
pkgver = "26.2.5"
pkgrel = 0
build_style = "meson"
configure_args = [
    "-Db_ndebug=true",
    "-Dbuild-tests=false",
    "-Ddefault_library=shared",
    "-Ddisplay-info=enabled",
    "-Degl=enabled",
    "-Dexpat=enabled",
    "-Dgallium-drivers=llvmpipe,softpipe",
    "-Dgallium-rusticl=false",
    "-Dgallium-va=disabled",
    "-Dgbm=enabled",
    "-Dgles1=enabled",
    "-Dgles2=enabled",
    "-Dglvnd=enabled",
    "-Dglx=disabled",
    "-Dhtml-docs=disabled",
    "-Dlibunwind=disabled",
    "-Dllvm=enabled",
    "-Dlmsensors=disabled",
    "-Dopengl=true",
    "-Dplatforms=wayland",
    "-Dshared-llvm=enabled",
    "-Dtools=",
    "-Dvideo-codecs=",
    "-Dvulkan-drivers=",
    "-Dxmlconfig=disabled",
    "-Dzlib=enabled",
    "-Dzstd=enabled",
]
meson_impl = "meson"
hostmakedepends = [
    "bison",
    "flex",
    "meson-real",
    "pkgconf",
    "python",
    "python-mako",
    "python-packaging",
    "python-pyyaml",
    "samurai",
    "wayland-progs",
]
makedepends = [
    "libdisplay-info-devel",
    "libdrm-devel",
    "libexpat-devel",
    "libffi8-devel",
    "libglvnd-devel",
    "linux-headers",
    "llvm-devel",
    "wayland-devel",
    "wayland-protocols",
    "zlib",
    "zstd-devel",
]
depends = ["libglvnd"]
provides = [self.with_pkgver("libglvnd-vendor")]
pkgdesc = "Mesa 3D graphics library"
license = "MIT"
url = "https://www.mesa3d.org"
source = f"https://archive.mesa3d.org/mesa-{pkgver}.tar.xz"
sha256 = "794b3d1729075dae7ebd47c7283b7ca0cdb5dec668f7f11cc0a5d82f6138a0a5"
# no X11, no Vulkan, no hardware drivers in this build
options = ["!check", "!cross", "linkundefver", "!lto", "!scanshlibs"]


def init_configure(self):
    self.configure_args += [f"-Dbackend_max_links={min(4, self.make_jobs)}"]


def post_install(self):
    self.install_license("docs/license.rst")


@subpackage("mesa-gbm-libs")
def _(self):
    self.pkgdesc = "Generic Buffer Management"
    self.renames = ["libgbm"]
    return ["usr/lib/gbm", "usr/lib/libgbm.so.*"]


@subpackage("mesa-gbm-devel")
def _(self):
    self.pkgdesc = "Generic Buffer Management"
    self.renames = ["libgbm-devel"]
    self.depends += [self.parent]
    return [
        "usr/include/gbm*.h",
        "usr/lib/libgbm.so",
        "usr/lib/pkgconfig/gbm.pc",
    ]


@subpackage("mesa-libgallium")
def _(self):
    self.pkgdesc = "Mesa gallium loader"
    self.renames = ["libglapi", "mesa-glapi-libs"]
    return ["usr/lib/libgallium-*.so"]



@subpackage("mesa-devel")
def _(self):
    self.depends += [self.parent, self.with_pkgver("mesa-gbm-devel"), "libglvnd-devel"]
    return self.default_devel()
