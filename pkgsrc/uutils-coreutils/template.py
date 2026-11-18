pkgname = "uutils-coreutils"
pkgver = "0.12.0"
pkgrel = 1
hostmakedepends = ["cargo-bootstrap", "rust"]
pkgdesc = "Cross-platform Rust rewrite of the GNU coreutils"
license = "MIT"
url = "https://uutils.github.io/coreutils"
source = f"https://github.com/uutils/coreutils/archive/refs/tags/{pkgver}.tar.gz"
sha256 = "4fb327655cb4ffcbf2f16550cf9234079ffe839692f7aa1a6eda104af684e122"
# tests take a long time and need special harnesses
options = ["!check"]

_cargo_env = {
    "CARGO_HOME": "/cbuild_cache/cargo",
    "CARGO_NET_OFFLINE": "true",
}


def prepare(self):
    self.do(
        "cargo",
        "fetch",
        "--locked",
        env={"CARGO_HOME": "/cbuild_cache/cargo"},
        allow_network=True,
    )


def build(self):
    self.do(
        "cargo",
        "build",
        "--release",
        "--locked",
        "--features",
        "unix,uudoc",
        env=_cargo_env,
    )
    # single multicall binary; dispatch is based on argv[0]
    res = self.do(
        "./target/release/coreutils", "--list", capture_output=True, env=_cargo_env
    )
    (self.cwd / "progs").write_text(res.stdout.decode())
    # generate one man page per utility; uudoc writes them to stdout
    self.do(
        "sh",
        "-c",
        "mkdir -p mandir && "
        "while read -r p; do ./target/release/uudoc manpage \"$p\" "
        '> "mandir/$p.1"; done < progs',
    )


def install(self):
    # install only into gnubin so sbase/ubase stay in charge of /usr/bin
    self.install_dir("usr/gnubin")
    self.install_file("target/release/coreutils", "usr/gnubin", 0o755)
    for name in (self.cwd / "progs").read_text().split():
        self.install_link(f"usr/gnubin/{name}", "coreutils")
        self.install_file(f"mandir/{name}.1", "usr/share/man/man1")
    self.install_license("LICENSE")
