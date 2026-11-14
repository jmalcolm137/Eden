pkgname = "transmission"
pkgver = "3.00"
pkgrel = 3
build_style = "cmake"
configure_args = [
    "-DENABLE_GTK=OFF",
    "-DENABLE_QT=OFF",
    "-DENABLE_MAC=OFF",
    "-DENABLE_TESTS=OFF",
    "-DENABLE_NLS=OFF",
    "-DENABLE_UTILS=ON",
    "-DENABLE_CLI=ON",
    "-DINSTALL_DOC=OFF",
    "-DENABLE_UTP=ON",
    "-DUSE_SYSTEM_UTP=OFF",
    "-DUSE_SYSTEM_EVENT2=ON",
    "-DWITH_CRYPTO=openssl",
    "-DCMAKE_POLICY_VERSION_MINIMUM=3.5",
    "-DCMAKE_EXE_LINKER_FLAGS=/usr/lib/libbearssl.a -lz",
]
hostmakedepends = [
    "bearssl-devel-static",
    "cmake",
    "curl",
    "libevent",
    "libevent-devel",
    "libevent-devel-static",
    "libressl-devel",
    "linux-headers",
    "zlib-ng-compat-devel",
]
pkgdesc = "BitTorrent client"
license = "GPL-2.0-or-later"
url = "https://transmissionbt.com"
source = "https://github.com/transmission/transmission-releases/raw/master/transmission-3.00.tar.xz"
sha256 = "9144652fe742f7f7dd6657716e378da60b751aaeda8bef8344b3eefc4db255f2"
# no test suite in the Oasis recipe
options = ["!check"]


def pre_configure(self):
    for p in (self.cwd / "third-party").rglob("CMakeLists.txt"):
        lines = p.read_text().splitlines()
        lines = [
            "cmake_minimum_required(VERSION 3.5)"
            if line.strip().startswith("cmake_minimum_required")
            else line
            for line in lines
        ]
        p.write_text("\n".join(lines) + "\n")
