pkgname = "ripgrep"
pkgver = "15.1.0"
pkgrel = 0
build_style = "cargo"
make_build_args = ["--features", "pcre2"]
make_install_args = ["--features", "pcre2"]
hostmakedepends = ["cargo-bootstrap", "pkgconf", "rust"]
makedepends = ["pcre2-devel"]
pkgdesc = "Line-oriented search tool that recursively searches directories"
license = "Unlicense OR MIT"
url = "https://github.com/BurntSushi/ripgrep"
source = f"{url}/archive/refs/tags/{pkgver}.tar.gz"
sha256 = "046fa01a216793b8bd2750f9d68d4ad43986eb9c0d6122600f993906012972e8"
# tests need a git checkout and write outside the sandbox
options = ["!check"]


def post_build(self):
    # ripgrep generates its own man page and completion scripts
    rg = f"target/{self.profile.triplet}/release/rg"
    for kind, out in (
        ("man", "rg.1"),
        ("complete-bash", "rg.bash"),
        ("complete-zsh", "rg.zsh"),
        ("complete-fish", "rg.fish"),
    ):
        self.do("sh", "-c", f"./{rg} --generate {kind} > {out}")


def post_install(self):
    self.install_man("rg.1")
    self.install_file(
        "rg.bash", "usr/share/bash-completion/completions", name="rg"
    )
    self.install_file("rg.zsh", "usr/share/zsh/site-functions", name="_rg")
    self.install_file(
        "rg.fish", "usr/share/fish/vendor_completions.d", name="rg.fish"
    )
    self.install_license("LICENSE-MIT")
    self.install_license("UNLICENSE")
