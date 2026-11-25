pkgname = "go"
pkgver = "1.27.4"
pkgrel = 0
archs = ["x86_64"]
hostmakedepends = ["bash", "clang", "go-bootstrap"]
makedepends = ["linux-headers", "musl-devel"]
# cgo programs need a C toolchain and the libc headers at build time
depends = ["clang", "linux-headers", "musl-devel"]
pkgdesc = "Go programming language"
license = "BSD-3-Clause"
url = "https://go.dev"
source = f"https://go.dev/dl/go{pkgver}.src.tar.gz"
sha256 = "73cfb8571aec0c01177687db87163d46aa20e9779672772891aa17654d9a6099"
# Go's test suite needs network and a different filesystem layout
options = ["!check", "!lto", "!strip"]


def _env(self):
    cwd = self.chroot_cwd
    return {
        "GOROOT_BOOTSTRAP": "/usr/lib/go-bootstrap",
        "GOROOT": str(cwd),
        "GOROOT_FINAL": "/usr/lib/go",
        "GOBIN": str(cwd / "bin"),
        "GOTOOLCHAIN": "local",
        "GOOS": "linux",
        "GOARCH": self.profile.goarch,
        "CC": "clang",
        "CXX": "clang++",
    }


def post_patch(self):
    # never download toolchains from the network
    p = self.cwd / "go.env"
    text = p.read_text()
    if "GOTOOLCHAIN=auto" not in text:
        self.error("unexpected go.env contents")
    p.write_text(text.replace("GOTOOLCHAIN=auto", "GOTOOLCHAIN=local"))


def build(self):
    self.do("./make.bash", env=_env(self), wrksrc="src")


def install(self):
    src = self.cwd / "src"

    # tests and their data are not needed by the installed toolchain
    tests = list(src.rglob("*_test.go"))
    for p in tests:
        p.unlink()
    for p in list(src.rglob("testdata")):
        self.rm(p, recursive=True)
    for pattern in ("*.rc", "*.bat"):
        for p in list(src.rglob(pattern)):
            p.unlink()

    for d in ["pkg/obj", "pkg/bootstrap"]:
        p = self.cwd / d
        if p.exists():
            self.rm(p, recursive=True)

    self.install_dir("usr/lib/go")
    for d in ["bin", "pkg", "src", "lib", "misc"]:
        self.install_files(self.cwd / d, "usr/lib/go")
    for f in ["go.env", "VERSION"]:
        self.install_file(self.cwd / f, "usr/lib/go")
    self.install_dir("usr/bin")
    self.install_link("usr/bin/go", "../lib/go/bin/go")
    self.install_link("usr/bin/gofmt", "../lib/go/bin/gofmt")
    self.install_files(self.cwd / "doc", "usr/share/doc", name="go")
    self.install_license("LICENSE")
