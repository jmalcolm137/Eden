pkgname = "libffi"
pkgver = "3.3"
pkgrel = 2
# Oasis pkg/libffi/src
_commit = "5dcb741f1544c5e18c9dbf96aeb8b61cc556a616"
pkgdesc = "Foreign function interface library from Oasis"
license = "MIT"
url = "https://sourceware.org/libffi"
source = f"https://github.com/libffi/libffi/archive/{_commit}.tar.gz"
sha256 = "55cd09d7514cab7eaef79a774e76721965c9d7ba3fc031670ca978d4d7d1aada"
# no test suite
options = ["!check", "!lto"]

_common = [
    "src/prep_cif.c",
    "src/types.c",
    "src/raw_api.c",
    "src/java_raw_api.c",
    "src/closures.c",
]


def _target(self):
    match self.profile.arch:
        case "x86_64":
            return "X86_64", "x86", [
                "src/x86/ffi64.c",
                "src/x86/unix64.S",
                "src/x86/ffiw64.c",
                "src/x86/win64.S",
            ]
        case "aarch64":
            return "AARCH64", "aarch64", [
                "src/aarch64/ffi.c",
                "src/aarch64/sysv.S",
            ]
        case "riscv64":
            return "RISCV", "riscv", [
                "src/riscv/ffi.c",
                "src/riscv/sysv.S",
            ]
        case _:
            self.error(f"unsupported architecture {self.profile.arch}")


def pre_build(self):
    self.cp(self.files_path / "fficonfig.h", "fficonfig.h")
    for p in sorted(self.files_path.glob("0*.patch")):
        self.cp(p, p.name)
        self.do("patch", "-p1", "-i", p.name)

    name, archdir, _ = _target(self)
    text = (self.cwd / "include/ffi.h.in").read_text()
    text = text.replace("@VERSION@", "3.3")
    text = text.replace("@TARGET@", name)
    text = text.replace("@HAVE_LONG_DOUBLE@", "1")
    text = text.replace("@HAVE_LONG_DOUBLE_VARIANT@", "0")
    text = text.replace("@FFI_EXEC_TRAMPOLINE_TABLE@", "0")
    (self.cwd / "include/ffi.h").write_text(text)
    self.cp(f"src/{archdir}/ffitarget.h", "include/ffitarget.h")


def build(self):
    from cbuild.util import compiler

    _, _, arch_sources = _target(self)
    cc = compiler.C(self)
    objs = []
    flags = [
        "-Wall",
        "-fPIC",
        "-Wno-deprecated-declarations",
        "-DHAVE_CONFIG_H",
        "-I.",
        "-Iinclude",
        "-Isrc",
    ]
    self.mkdir("obj", parents=True)

    for src in _common + arch_sources:
        obj = "obj/" + src.replace("/", "_").removesuffix(".c").removesuffix(".S") + ".o"
        cc.invoke([src], obj, obj_file=True, flags=flags)
        objs.append(obj)

    self.do("ar", "rcs", "libffi.a", *objs)
    self.do(
        "clang",
        "-shared",
        "-Wl,-soname,libffi.so.8",
        "-o",
        "libffi.so.8.1.0",
        *objs,
    )


def install(self):
    self.install_file("libffi.a", "usr/lib")
    self.install_file("libffi.so.8.1.0", "usr/lib", mode=0o755)
    self.install_link("usr/lib/libffi.so.8", "libffi.so.8.1.0")
    self.install_file("include/ffi.h", "usr/include")
    self.install_file("include/ffitarget.h", "usr/include")
    self.install_file(self.files_path / "libffi.pc", "usr/lib/pkgconfig")
    self.install_license("LICENSE")
