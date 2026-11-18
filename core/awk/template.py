pkgname = "awk"
pkgver = "20260426"
pkgrel = 1
build_style = "makefile"
make_build_target = "a.out"
make_build_args = ["YACC=byacc -d -b awkgram", "HOSTCC=clang"]
hostmakedepends = ["byacc"]
makedepends = [
    "libatomic-chimera-devel-static",
    "libunwind-devel-static",
    "musl-devel-static",
]
pkgdesc = "One True awk from Oasis"
license = "custom:awk"
url = "https://github.com/onetrueawk/awk"
source = f"{url}/archive/refs/tags/{pkgver}.tar.gz"
sha256 = "7ae5b9fc6a8149bc45ea0ba3ba434a69a16d1460d19f6d01b6f04cc885b8e02b"
tool_flags = {"LDFLAGS": ["-static-pie"]}
# no tests; upstream's check target runs a large interactive regression suite
options = ["bootstrap", "!check"]


def post_patch(self):
    # The upstream makefile does not use LDFLAGS; add the static-pie link
    # directly to the awk rule.
    p = self.cwd / "makefile"
    text = p.read_text()
    text = text.replace(
        "$(CC) $(CFLAGS) awkgram.tab.o $(OFILES) $(ALLOC)  -lm",
        "$(CC) $(CFLAGS) -static-pie awkgram.tab.o $(OFILES) $(ALLOC)  -lm",
        1,
    )
    p.write_text(text)


def install(self):
    self.install_bin("a.out", name="awk")
    self.install_man("awk.1")
    self.install_license("LICENSE")
