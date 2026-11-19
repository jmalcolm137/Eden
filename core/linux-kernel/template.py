pkgname = "linux-kernel"
pkgver = "7.3.5"
pkgrel = 0
archs = ["x86_64"]
hostmakedepends = [
    "bc",
    "flex",
    "gmake",
    "kmod",
    "linux-headers",
    "openbsd",
    "perl",
    "python",
    "xz",
    "zstd-progs",
]
# objtool needs libelf; provided by the elftoolchain-devel package
depends = ["kmod"]
pkgdesc = "CachyOS-based Linux kernel built for baseline x86-64 v1"
license = "GPL-2.0-only"
url = "https://github.com/CachyOS/linux-cachyos"
source = [
    f"https://github.com/CachyOS/linux/releases/download/cachyos-{pkgver}-2/cachyos-{pkgver}-2.tar.gz",
]
sha256 = ["bb22ad99e1042fae883bab71366f8339367b74c045004fe92ad4923339092e07"]
# LTO, module signing and debug info are disabled in the config; no meaningful
# check target, and standard ELF checks do not apply to a kernel image
options = [
    "!check",
    "!strip",
    "!debug",
    "!lto",
    "!scanrundeps",
    "!scanshlibs",
    "textrels",
    "execstack",
    "foreignelf",
]


# the kernel's kconfig and dtc parsers are bison-generated; ship pregenerated
# sources behind a shim instead of building bison in the container


def _setup_bison(self):
    self.mkdir(".bison-pregen", parents=True)
    for f in (
        "parser.tab.c",
        "parser.tab.h",
        "dtc-parser.tab.c",
        "dtc-parser.tab.h",
    ):
        self.cp(self.files_path / "bison-pregen" / f, f".bison-pregen/{f}")
    self.mkdir("bison-shim", parents=True)
    p = self.cwd / "bison-shim" / "bison"
    self.cp(self.files_path / "bison-shim.sh", "bison-shim/bison")
    p.chmod(0o755)
    return str(self.chroot_cwd / "bison-shim")


def configure(self):
    self.cp(self.files_path / "config-x86_64", ".config")
    # sbase dd has no GNU status=none
    mk = self.cwd / "arch/x86/boot/Makefile"
    mk.write_text(mk.read_text().replace(" status=none", ""))
    # sbase ln has no -n
    amk = self.cwd / "arch/x86/Makefile"
    amk.write_text(amk.read_text().replace("ln -fsn", "ln -fs"))
    shim = _setup_bison(self)
    self.do(
        "gmake",
        "LLVM=1",
        "olddefconfig",
        env={"PATH": f"{shim}:/usr/gnubin:/usr/bin:/bin"},
    )


def build(self):
    shim = str(self.chroot_cwd / "bison-shim")
    self.do(
        "gmake",
        "LLVM=1",
        f"-j{self.make_jobs}",
        "bzImage",
        "modules",
        env={"PATH": f"{shim}:/usr/gnubin:/usr/bin:/bin"},
    )


def install(self):
    krel = (self.cwd / "include/config/kernel.release").read_text().strip()

    self.do(
        "gmake",
        "LLVM=1",
        f"INSTALL_MOD_PATH={self.chroot_destdir}/usr",
        "INSTALL_MOD_STRIP=1",
        "modules_install",
    )

    self.install_dir("boot")
    self.install_file("arch/x86/boot/bzImage", "boot", name=f"vmlinuz-{krel}")
    self.install_file(".config", "boot", name=f"config-{krel}")
    self.install_file("System.map", "boot", name=f"System.map-{krel}")
