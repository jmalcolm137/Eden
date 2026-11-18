pkgname = "libgcc-chimera"
pkgver = "22.1.8"
pkgrel = 0
archs = ["x86_64"]
makedepends = [
    "clang-rt-devel",
    "libunwind-devel",
    "linux-headers",
    "musl-devel",
]
depends = ["libunwind"]
pkgdesc = "Chimera shim for libgcc runtime compatibility"
license = "Apache-2.0 WITH LLVM-exception AND NCSA"
url = "https://llvm.org"
source = []
# shim only
options = ["!check", "!lto"]


def build(self):
    self.cp(self.files_path / "LICENSE.TXT", "LICENSE.TXT")

    majver = pkgver.split(".")[0]
    trip = self.profile.triplet
    builtins = f"/usr/lib/clang/{majver}/lib/{trip}/libclang_rt.builtins.a"

    self.do(
        self.get_tool("CC"),
        "-shared",
        "-fPIC",
        "-nodefaultlibs",
        "-Wl,-soname,libgcc_s.so.1",
        "-Wl,--no-undefined",
        "-Wl,--whole-archive",
        builtins,
        "-Wl,--no-as-needed",
        "-lc",
        "-lunwind",
        "-o",
        "libgcc_s.so.1",
    )

    (self.cwd / "libgcc_s.so").write_text(
        f"INPUT({builtins} -lunwind)\n"
    )


def install(self):
    self.install_lib("libgcc_s.so.1")
    self.install_lib("libgcc_s.so")
    self.install_license("LICENSE.TXT")
