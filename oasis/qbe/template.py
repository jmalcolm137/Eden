pkgname = "qbe"
pkgver = "1.3_git20260602"
pkgrel = 0
# Oasis pkg/qbe/src
_commit = "e786f06032fefa2e3790d6b1c9e31ed138f475a6"
archs = ["aarch64", "riscv64", "x86_64"]
build_style = "makefile"
pkgdesc = "QBE compiler backend from Oasis"
license = "MIT"
url = "https://c9x.me/compile"
source = f"https://github.com/omenos/mirror-qbe/archive/{_commit}.tar.gz"
sha256 = "5d314adc2613dfe500544119f190372b43606ead30fb5c637211b945c9f3770a"
# upstream tests need cross compilers and qemu
options = ["!check"]


def pre_build(self):
    match self.profile.arch:
        case "x86_64":
            deftgt = "T_amd64_sysv"
        case "aarch64":
            deftgt = "T_arm64"
        case "riscv64":
            deftgt = "T_rv64"
        case _:
            self.error(f"unknown architecture {self.profile.arch}")

    # Oasis pkg/qbe/config.h, selected per target
    with open(self.cwd / "config.h", "w") as f:
        f.write(f"#define Deftgt {deftgt}\n")


def post_install(self):
    self.install_license("LICENSE")
