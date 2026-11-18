pkgname = "doas"
pkgver = "6.3_p2"
pkgrel = 0
# upstream tag
_tag = "6.3p2"
hostmakedepends = ["byacc"]
makedepends = [
    "libatomic-chimera-devel-static",
    "musl-devel-static",
]
triggers = ["/usr/bin/doas"]
pkgdesc = "Execute commands as another user"
license = "BSD-2-Clause AND ISC AND BSD-3-Clause"
url = "https://github.com/slicer69/doas"
source = f"https://github.com/slicer69/doas/archive/refs/tags/{_tag}.tar.gz"
sha256 = "037813a404bfe35289f2c6cb22a8c4de6f636b2a491e546a90d2ae2afa54aa64"
file_modes = {"usr/bin/doas": ("root", "root", 0o4755)}
# upstream has no test suite
options = ["!check"]


def build(self):
    self.do(
        self.make_cmd,
        "CC=" + self.get_tool("CC"),
        "YACC=byacc",
        "PREFIX=/usr",
        "SYSCONFDIR=/etc",
        "CFLAGS="
        + self.get_cflags(shell=True)
        + " -D_GNU_SOURCE -DUSE_SHADOW -Icompat"
        + r" -DDOAS_CONF=\"/etc/doas.conf\"",
        "LDFLAGS="
        + self.get_ldflags(shell=True)
        + " -static-pie -unwindlib=none",
    )


def install(self):
    # doas is a setuid-root helper; PAM is unavailable in this tree, so the
    # package uses the libc shadow/crypt interfaces instead.
    self.install_file("doas", "usr/bin", mode=0o4755)
    self.install_file(
        "doas.1.final", "usr/share/man/man1", name="doas.1", mode=0o644
    )
    self.install_file(
        "doas.conf.5.final", "usr/share/man/man5", name="doas.conf.5", mode=0o644
    )
    self.install_license("LICENSE")
