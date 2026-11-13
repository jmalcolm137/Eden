pkgname = "libdrm"
pkgver = "2.4.120"
pkgrel = 0
# Oasis pkg/libdrm/src
_commit = "6bfcfc725fbe0ece0918535556d61ee567b1ffff"
build_style = "meson"
configure_args = [
    "-Dintel=disabled",
    "-Dradeon=disabled",
    "-Damdgpu=disabled",
    "-Dnouveau=disabled",
    "-Dvmwgfx=disabled",
    "-Dfreedreno=disabled",
    "-Dvc4=disabled",
    "-Detnaviv=disabled",
    "-Dtests=false",
    "-Dman-pages=disabled",
    "-Dvalgrind=disabled",
    "-Dcairo-tests=disabled",
]
hostmakedepends = ["python"]
makedepends = ["linux-headers"]
pkgdesc = "Direct Rendering Manager library"
license = "MIT"
url = "https://gitlab.freedesktop.org/mesa/drm"
source = f"{url}/-/archive/{_commit}/drm-{_commit}.tar.gz"
sha256 = "8db2068bfdf1504b2ad8fcf75fd4ccfd7d858f2b4d70688e3cadb373f74b480f"
# no test suite in the Oasis recipe
options = ["!check"]


@subpackage("libdrm-devel")
def _(self):
    return self.default_devel()


def post_install(self):
    self.install_license(self.files_path / "LICENSE")
