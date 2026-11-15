pkgname = "ffmpeg"
pkgver = "7.0.2"
pkgrel = 1
build_style = "makefile"
configure_args = [
    "--cc=clang",
    "--enable-cross-compile",
    "--target-os=linux",
    "--arch=x86_64",
    "--disable-doc",
    "--disable-ffplay",
    "--enable-shared",
    "--disable-static",
    "--enable-libdav1d",
    "--enable-libass",
    "--enable-libopus",
    "--enable-alsa",
    "--enable-openssl",
    "--enable-libdrm",
    "--disable-libv4l2",
    "--disable-vaapi",
    "--disable-vdpau",
    "--disable-vulkan",
]
configure_env = {"CC": "clang", "CXX": "clang++"}
make_dir = "build"
make_use_env = True
hostmakedepends = ["pkgconf"]
makedepends = [
    "alsa-lib-devel",
    "dav1d-devel",
    "libass-devel",
    "libdrm-devel",
    "libressl-devel",
    "linux-headers",
    "nasm",
    "opus-devel",
    "opus-devel-static",
    "zlib-static",
]
pkgdesc = "Multimedia framework"
license = "GPL-2.0-or-later"
url = "https://ffmpeg.org"
source = f"{url}/releases/ffmpeg-{pkgver}.tar.xz"
sha256 = "8646515b638a3ad303e23af6a3587734447cb8fc0a0c064ecdb8e95c4fd8b389"
# no test suite in the Oasis recipe
options = ["!check"]


def configure(self):
    self.mkdir("build", parents=True)
    self.do(
        str(self.chroot_cwd / "configure"),
        "--prefix=/usr",
        "--cc=clang",
        "--disable-doc",
        "--disable-ffplay",
        "--enable-shared",
        "--disable-static",
        "--enable-libdav1d",
        "--enable-libass",
        "--enable-libopus",
        "--enable-alsa",
        "--enable-openssl",
        "--enable-libdrm",
        "--disable-libv4l2",
        "--disable-indev=v4l2",
        "--disable-outdev=v4l2",
        "--disable-v4l2-m2m",
        "--disable-vaapi",
        "--disable-vdpau",
        "--disable-vulkan",
        wrksrc=self.chroot_cwd / "build",
    )


@subpackage("ffmpeg-devel")
def _(self):
    return self.default_devel()
