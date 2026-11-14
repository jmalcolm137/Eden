pkgname = "mgba"
pkgver = "0.8.4"
pkgrel = 4
build_style = "cmake"
configure_args = [
    "-DBUILD_QT=OFF",
    "-DBUILD_SDL=OFF",
    "-DBUILD_GL=OFF",
    "-DBUILD_GLES2=OFF",
    "-DBUILD_SUITE=OFF",
    "-DBUILD_TEST=OFF",
    "-DBUILD_STATIC=ON",
    "-DBUILD_SHARED=OFF",
    "-DCMAKE_POLICY_VERSION_MINIMUM=3.5",
    "-DUSE_DEBUGGERS=OFF",
    "-DUSE_DISCORD_RPC=OFF",
    "-DUSE_SQLITE3=OFF",
    "-DUSE_LZMA=OFF",
]
hostmakedepends = ["cmake"]
makedepends = ["libpng", "zlib-static"]
pkgdesc = "Game Boy Advance emulator"
license = "MPL-2.0"
url = "https://mgba.io"
source = f"https://github.com/mgba-emu/mgba/archive/refs/tags/{pkgver}.tar.gz"
sha256 = "6b94873dac9040fd6fd9f13f76dc48f342e954f3b4cf82717b59601c3a32b72c"
# no test suite in the Oasis recipe
options = ["!lto", "!check"]
