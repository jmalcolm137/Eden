pkgname = "cmake"
pkgver = "4.4.3"
pkgrel = 0
# x86_64 only for the initial source-bootstrap toolchain; other
# architectures can be restored once this path is working.
archs = ["x86_64"]
build_style = "configure"
configure_args = [
    "--prefix=/usr",
    "--mandir=/share/man",
    "--docdir=/share/doc/cmake",
    "--generator=Ninja",
    f"--parallel={self.conf_jobs}",
    "--",
    "-DCMAKE_INSTALL_LIBDIR=lib",
    "-DCMAKE_USE_OPENSSL=OFF",
]
make_cmd = "samu"
hostmakedepends = ["samurai"]
makedepends = ["linux-headers"]
pkgdesc = "Cross-platform, open source build system"
license = "BSD-3-Clause"
url = "https://cmake.org"
source = f"https://www.cmake.org/files/v{pkgver[:-2]}/cmake-{pkgver}.tar.gz"
sha256 = "c46400618b4f1f2b43507f24fb22f3ae830c3416cf23b776e16e1d413aa892f0"
# prevent cmake self-bootstrap false positive nonsense
tool_flags = {
    "CXXFLAGS": ["-Wno-unused-command-line-argument"],
}
hardening = ["vis", "!int"]
# bootstrap build: no check tooling or LTO
options = ["bootstrap", "!check", "!lto"]

# need to use bundled jsoncpp (i.e. --system-jsoncpp is not possible) as
# the two build systems that offers are meson and cmake - cmake cannot be
# used for obvious reasons, meson can't either as during stage 2 at the
# point cmake is built, meson is not yet available, but no big deal
# stage-2 system-library mode is intentionally skipped for the bootstrap


# if cross compiling, use host cmake outright
if self.profile.cross:
    build_style = "cmake"
    configure_args = [
        "-DCMAKE_MAN_DIR=/share/man",
        "-DCMAKE_DOC_DIR=/share/doc/cmake",
        "-DCMAKE_USE_SYSTEM_LIBARCHIVE=ON",
        "-DCMAKE_USE_SYSTEM_ZLIB=ON",
        "-DCMAKE_USE_SYSTEM_BZIP2=ON",
        "-DCMAKE_USE_SYSTEM_LIBLZMA=ON",
        "-DCMAKE_USE_SYSTEM_ZSTD=ON",
        "-DCMAKE_USE_SYSTEM_CURL=ON",
        "-DCMAKE_USE_SYSTEM_NGHTTP2=ON",
        "-DCMAKE_USE_SYSTEM_EXPAT=ON",
        "-DCMAKE_USE_SYSTEM_LIBUV=ON",
        "-DCMAKE_USE_SYSTEM_LIBRHASH=ON",
    ]
    hostmakedepends += ["cmake"]


def post_install(self):
    self.install_license("LICENSE.rst")
    self.cp("Utilities/KWIML/Copyright.txt", "KWIML-Copyright.txt")
    self.install_license("KWIML-Copyright.txt")
