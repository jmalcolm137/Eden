pkgname = "uutils-findutils"
pkgver = "0.11.0"
pkgrel = 0
hostmakedepends = ["cargo-bootstrap", "rust"]
pkgdesc = "Rust implementation of GNU findutils"
license = "MIT"
url = "https://github.com/uutils/findutils"
source = f"https://github.com/uutils/findutils/archive/refs/tags/{pkgver}.tar.gz"
sha256 = "43d1fbb69a0e67e708435bd104966d1dd61357755452b733db9dabfd66cbf974"
# tests need GNU find/xargs and write outside the sandbox
options = ["!check"]

_cargo_env = {
    "CARGO_HOME": "/cbuild_cache/cargo",
    "CARGO_NET_OFFLINE": "true",
}

# upstream does not ship man pages, so generate a minimal page per tool
_mans = {
    "find": "search for files in a directory hierarchy",
    "locate": "list files in databases that match a pattern",
    "updatedb": "update a file name database",
    "xargs": "build and execute command lines from standard input",
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
    self.do("cargo", "build", "--release", "--locked", env=_cargo_env)

    self.mkdir("mandir", parents=True)
    for name, desc in _mans.items():
        res = self.do(
            f"./target/release/{name}", "--help", capture_output=True, env=_cargo_env
        )
        text = res.stdout.decode() or res.stderr.decode()
        # roff treats a leading dot or apostrophe as a request
        body = "\n".join(
            "\\&" + line if line[:1] in (".", "'") else line
            for line in text.splitlines()
        )
        page = (
            f".TH {name.upper()} 1\n"
            ".SH NAME\n"
            f"{name} \\- {desc}\n"
            ".SH SYNOPSIS\n"
            f".B {name}\n"
            "[OPTION]... [ARG]...\n"
            ".SH DESCRIPTION\n"
            ".nf\n"
            f"{body}\n"
            ".fi\n"
        )
        (self.cwd / "mandir" / f"{name}.1").write_text(page)


def install(self):
    # install only into gnubin so the sbase/ubase tools stay in charge
    self.install_dir("usr/gnubin")
    for name in _mans:
        self.install_file(f"target/release/{name}", "usr/gnubin", 0o755)
        self.install_file(f"mandir/{name}.1", "usr/share/man/man1")
    self.install_license("LICENSE")
