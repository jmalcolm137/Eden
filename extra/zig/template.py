pkgname = "zig"
pkgver = "0.17.1"
pkgrel = 0
# Eden's LLVM is built for X86 only
archs = ["x86_64"]
build_style = "cmake"
configure_args = [
    # dodge -Dstrip, but keep debug info out of the huge generated C files
    "-DCMAKE_BUILD_TYPE=RelWithDebInfo",
    "-DCMAKE_C_FLAGS_RELWITHDEBINFO=-O2 -DNDEBUG",
    "-DCMAKE_CXX_FLAGS_RELWITHDEBINFO=-O2 -DNDEBUG",
    "-DZIG_PIE=ON",
    # there are no per-component shared LLVM libraries in Eden
    "-DZIG_STATIC_LLVM=ON",
    "-DZIG_STATIC_ZLIB=ON",
    "-DZIG_STATIC_ZSTD=ON",
    "-DZIG_TARGET_MCPU=baseline",
    # langref doctests compile native examples without an explicit target
    "-DZIG_EXTRA_BUILD_ARGS=-Dno-langref",
    "-DZIG_USE_LLVM_CONFIG=ON",
    "-DZIG_TARGET_TRIPLE=x86_64-linux-musl",
]
hostmakedepends = [
    "cmake",
    "pkgconf",
    "samurai",
]
makedepends = [
    "clang-devel",
    "clang-devel-static",
    "linux-headers",
    "lld-devel",
    "lld-devel-static",
    "llvm-devel",
    "llvm-devel-static",
    "netbsd-curses-devel",
    "zlib",
    "zstd-devel",
    "zstd-devel-static",
]
pkgdesc = "Zig programming language toolchain"
license = "MIT"
url = "https://github.com/ziglang/zig"
source = f"https://ziglang.org/download/{pkgver}/zig-{pkgver}.tar.xz"
sha256 = "1e89bf06610b769a8c77676c6c8d54b093a0db60f4891f2f91014829012f0e24"
# lighten up the build, only applies to bootstrap and just slows down the build
tool_flags = {"CFLAGS": ["-U_FORTIFY_SOURCE"]}
hardening = ["!int", "!scp", "!ssp", "!var-init"]
# the test suite's configure step fails in the offline cbuild sandbox
options = ["!lto", "!check"]

# The CMake bootstrap builds its stage2 compiler from the prebuilt
# stage1/zig1.wasm, which cannot carry downstream patches. Bootstrap it for
# the musl target so it does not need native libc detection. The
# compiler-rt-crt patch teaches the resulting stage3 compiler about
# compiler-rt's CRT names, so installed programs link against Eden's musl
# rather than Zig's bundled copy.


def post_patch(self):
    # Zig insists on an all-target LLVM; the local toolchain only carries
    # X86, which is all Eden targets anyway
    cmakef = self.cwd / "cmake/Findllvm.cmake"
    lines = cmakef.read_text().splitlines()
    for i, line in enumerate(lines):
        if line.strip().startswith('set(ZIG_LLVM_REQUIRED_TARGETS "'):
            lines[i] = '    set(ZIG_LLVM_REQUIRED_TARGETS "X86")'
            break
    else:
        self.error("unexpected LLVM target check in Findllvm.cmake")
    cmakef.write_text("\n".join(lines) + "\n")

    # zig2.c is hundreds of megabytes of generated C; debug info and the
    # default optimization level make clang run out of memory
    cmakef = self.cwd / "CMakeLists.txt"
    old = (
        'set(ZIG2_COMPILE_FLAGS "-std=c99 -Oz -fno-sanitize=undefined '
        '-fno-stack-protector -fno-strict-aliasing")'
    )
    new = (
        'set(ZIG2_COMPILE_FLAGS "-std=c99 -O1 -g0 -fno-sanitize=undefined '
        '-fno-stack-protector -fno-strict-aliasing")'
    )
    text = cmakef.read_text()
    if old not in text:
        self.error("unexpected zig2 compile flags")
    cmakef.write_text(text.replace(old, new))

    # the compiler registers every LLVM backend it knows about; restrict it
    # to the X86 backend that the local LLVM actually carries
    llvmzig = self.cwd / "src/codegen/llvm.zig"
    text = llvmzig.read_text()
    start = text.index("pub fn initializeLLVMTarget")
    llvmzig.write_text(
        text[:start]
        + """pub fn initializeLLVMTarget(io: Io, arch: std.Target.Cpu.Arch) void {
    target_registry_mutex.lockUncancelable(io);
    defer target_registry_mutex.unlock(io);

    switch (arch) {
        .x86, .x86_64 => {
            bindings.LLVMInitializeX86Target();
            bindings.LLVMInitializeX86TargetInfo();
            bindings.LLVMInitializeX86TargetMC();
            bindings.LLVMInitializeX86AsmPrinter();
            bindings.LLVMInitializeX86AsmParser();
        },
        else => unreachable,
    }
}
"""
    )


def check(self):
    self.do(
        self.make_dir + "/stage3/bin/zig",
        "build",
        "test",
        "--summary",
        "all",
        "-Dcpu=baseline",
        "-Dskip-debug",
        "-Dskip-non-native",
        "-Dskip-release-safe",
        "-Dskip-release-small",
    )


def install(self):
    self.install_license("LICENSE")
    self.install_files(f"{self.make_dir}/stage3/bin", "usr")
    self.install_files(f"{self.make_dir}/stage3/lib", "usr")
