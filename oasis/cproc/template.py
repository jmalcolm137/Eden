pkgname = "cproc"
pkgver = "0_git20260528"
pkgrel = 2
# Oasis pkg/cproc/src
_commit = "6e8426cba04bb95952355e3967b749b47037c7c2"
archs = ["aarch64", "riscv64", "x86_64"]
build_style = "makefile"
# cproc's driver needs a preprocessor, QBE, an assembler and a linker;
# mcpp preprocesses and GNU binutils assemble/link (no clang/llvm).
depends = ["binutils", "mcpp", "musl-devel", "musl-devel-static", "qbe"]
pkgdesc = "C11 compiler using the QBE compiler backend"
license = "ISC AND MIT AND Unlicense"
url = "https://git.sr.ht/~mcf/cproc"
source = f"{url}/archive/{_commit}.tar.gz"
sha256 = "f2b955acd2729dfcac184ccd0f8b3afc1680bebf315f141fe6115888bdee2445"


def pre_build(self):
    self.cp(self.files_path / "config.h", "config.h")

    match self.profile.arch:
        case "x86_64":
            target = "x86_64-linux-musl"
            ldso = "/lib/ld-musl-x86_64.so.1"
        case "aarch64":
            target = "aarch64-linux-musl"
            ldso = "/lib/ld-musl-aarch64.so.1"
        case "riscv64":
            target = "riscv64-linux-musl"
            ldso = "/lib/ld-musl-riscv64.so.1"
        case _:
            self.error(f"unknown architecture {self.profile.arch}")

    # rewrite the target and dynamic linker for non-x86_64 profiles
    with open(self.cwd / "config.h") as f:
        conf = f.read()
    conf = conf.replace("x86_64-linux-musl", target)
    conf = conf.replace("/lib/ld-musl-x86_64.so.1", ldso)
    with open(self.cwd / "config.h", "w") as f:
        f.write(conf)


def post_install(self):
    self.install_license("LICENSE")
