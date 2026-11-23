pkgname = "rust"
pkgver = "1.99.1"
pkgrel = 0
# x86_64 only until the bootstrap chain is available for other arches
archs = ["x86_64"]
hostmakedepends = [
    "cargo-bootstrap",
    "cmake",
    "curl",
    "libffi8-devel",
    "libressl-devel",
    "llvm-devel",
    "llvm-tools",
    "musl-devel",
    "musl-devel-static",
    "pkgconf",
    "python",
    "rust-bootstrap",
    "zlib",
    "zstd-devel",
]
makedepends = [
    "libffi8-devel",
    "libressl-devel",
    "llvm-devel",
    "zlib",
    "zstd-devel",
]
depends = ["clang", "libressl", "musl-devel", "zlib-shared"]
pkgdesc = "Rust programming language"
license = "MIT OR Apache-2.0"
url = "https://rust-lang.org"
source = f"https://static.rust-lang.org/dist/rustc-{pkgver}-src.tar.xz"
sha256 = "6451598a99e77f07571960f6b21d577399d3a30f33e80cbd2e3a4aae6535d265"
env = {
    "SSL_CERT_FILE": "/etc/ssl/certs/ca-certificates.crt",
    "OPENSSL_NO_VENDOR": "1",
    "RUST_BACKTRACE": "1",
}
# skipped: rust's self-check and cross-version LTO
options = ["!check", "!lto"]

def configure(self):
    trip = self.profile.triplet

    with self.use_profile("host") as hpf:
        host_trip = hpf.triplet

    with open(self.cwd / "bootstrap.toml", "w") as cfg:
        cfg.write(
            f"""
change-id = 160100

[llvm]
ninja = false
link-shared = true
static-libstdcpp = false
use-libcxx = true

[build]
description = 'Oasis'
build = '{host_trip}'
host = ['{trip}']
target = ['{trip}']
cargo = '/usr/bin/cargo'
rustc = '/usr/bin/rustc'
docs = false
python = 'python'
locked-deps = true
vendor = true
extended = false
tools = ['cargo', 'rustdoc']
profiler = false
local-rebuild = false

[install]
prefix = '/usr'

[rust]
optimize = true
debug = false
backtrace-on-ice = true
codegen-units = 1
codegen-units-std = 1
debuginfo-level = 0
debuginfo-level-std = 0
lto = 'thin-local'
incremental = false
channel = 'stable'

rpath = false
frame-pointers = true
deny-warnings = false
llvm-libunwind = 'system'

[target.{trip}]
cc = '{self.get_tool("CC", target="host")}'
cxx = '{self.get_tool("CXX", target="host")}'
ar = '/usr/bin/llvm-ar'
ranlib = '/usr/bin/llvm-ranlib'
linker = '{self.get_tool("CC", target="host")}'
llvm-config = '/usr/bin/llvm-config'
crt-static = false
"""
        )


def build(self):
    benv = {
        "CARGO_HOME": str(self.chroot_cwd / ".cargo"),
    }
    self.do(
        "env",
        "-u",
        "PKG_CONFIG",
        "-u",
        "CFLAGS",
        "-u",
        "CXXFLAGS",
        "--",
        "python",
        "x.py",
        "build",
        "--stage",
        "2",
        "--jobs",
        str(self.make_jobs),
        env=benv,
    )


def install(self):
    self.do(
        "python",
        "x.py",
        "install",
        "--jobs",
        str(self.make_jobs),
        env={"DESTDIR": str(self.chroot_destdir)},
    )

    self.install_license("COPYRIGHT")
    self.install_license("LICENSE-MIT")

    # upstream installs this to /etc; it belongs with the rust data
    self.rename(
        "etc/target-spec-json-schema.json",
        "usr/share/rust/target-spec-json-schema.json",
        relative=False,
    )
    self.uninstall("etc", missing_ok=True)

    trip = self.profile.triplet
    self.uninstall(f"usr/lib/rustlib/{trip}/bin", missing_ok=True)
    self.uninstall("usr/etc", missing_ok=True)



def post_patch(self):
    # the bootstrap rustc resolves target libraries via lib64; the
    # stage0 sysroot is assembled from /usr/lib without that compat link
    p = self.cwd / "src/bootstrap/src/core/build_steps/compile.rs"
    text = p.read_text()
    old = """            builder.cp_link_r(
                &builder.initial_sysroot.join("lib/rustlib"),
                &sysroot.join("lib/rustlib"),
            );"""
    new = old + """
            let sysroot_lib64 = sysroot.join("lib64");
            if sysroot_lib64.is_dir() {
                let _ = std::fs::remove_dir_all(&sysroot_lib64);
            }
            if !sysroot_lib64.exists() {
                let _ = std::os::unix::fs::symlink("lib", &sysroot_lib64);
            }"""
    if old not in text:
        self.error("failed to patch bootstrap stage0 sysroot")
    p.write_text(text.replace(old, new))

    # patches touch vendored crates, so drop the file checksums
    from cbuild.util import cargo

    for d in (self.cwd / "vendor").iterdir():
        if d.is_dir() and (d / ".cargo-checksum.json").is_file():
            cargo.clear_vendor_checksums(self, d.name)
