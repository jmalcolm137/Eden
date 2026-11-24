pkgname = "gleam"
pkgver = "1.19.2"
pkgrel = 0
build_style = "cargo"
# only the compiler binary; the workspace also carries test and benchmark crates
make_build_args = ["-p", "gleam"]
hostmakedepends = ["cargo-bootstrap", "rust"]
depends = ["ca-certificates"]
pkgdesc = "Statically typed language for the Erlang VM and JavaScript"
license = "Apache-2.0"
url = "https://gleam.run"
source = f"https://github.com/gleam-lang/gleam/archive/refs/tags/v{pkgver}.tar.gz"
sha256 = "d8796325dad02802dccc91568a90a00e43247cad1d87ddbd9779a99d3c435d61"
# tests need git, network access and the Erlang/JavaScript runtimes
options = ["!check"]


def prepare(self):
    self.cargo.vendor()

    from cbuild.util import cargo as cargo_util

    # aws-lc-sys probes for -Wa,--debug-prefix-map and then passes it to the
    # assembler; clang's integrated assembler rejects it
    crate = next((self.cwd / "vendor").glob("aws-lc-sys-*"))
    builder = crate / "builder/cc_builder.rs"
    old = "cc_build.asm_flag(asm_flag);"
    text = builder.read_text()
    if old not in text:
        self.error("unexpected aws-lc-sys assembly flag handling")
    builder.write_text(text.replace(old, "let _ = asm_flag;"))
    cargo_util.clear_vendor_checksums(self, crate.name)


def install(self):
    from cbuild.util import cargo

    self.install_bin(cargo.target_path(self, "gleam"))
    self.install_license("LICENCE")
