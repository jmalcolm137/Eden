pkgname = "git"
pkgver = "2.54.0"
pkgrel = 0
# Oasis pkg/git/src (git.git v2.54.0)
_commit = "94f057755b7941b321fd11fec1b2e3ca5313a4e0"
hostmakedepends = ["pkgconf"]
makedepends = ["bearssl-devel", "curl", "zlib-ng-compat-devel"]
depends = ["zlib-ng-compat"]
pkgdesc = "Fast, scalable, distributed revision control system"
license = "GPL-2.0-only"
url = "https://git-scm.com"
source = [
    f"https://github.com/git/git/archive/{_commit}.tar.gz",
    f"https://www.kernel.org/pub/software/scm/git/git-manpages-{pkgver}.tar.gz",
]
source_paths = ["", "man"]
sha256 = [
    "cfb1944f14aa15bd2f59c0b5774aa63a37a448aa1b1b8ab4d5405ea5f22276ea",
    "2d0950c3dd3346f1072e5791ac308961639828f2b6ba91927e64fed97a1bd550",
]
# Oasis pkg/git config.h. HTTP/IMAP transport uses the Oasis static
# libcurl.a from core/curl (BearSSL + zlib).
# no tests; upstream's suite needs a full test harness
options = ["!check"]


def configure(self):
    self.cp(self.files_path / "oasis-config.h", ".")

    cfl = self.get_cflags(shell=True)
    ldfl = self.get_ldflags(shell=True)

    with open(self.cwd / "config.mak", "w") as cf:
        cf.write(
            f"""\
prefix = /usr
gitexecdir = /usr/lib/git-core
template_dir = /usr/share/git-core/templates
sysconfdir = /etc
mandir = /usr/share/man
infodir = /usr/share/info
localedir = /usr/share/locale
CC = {self.get_tool("CC")}
AR = {self.get_tool("AR")}
CFLAGS = {cfl} -include oasis-config.h -DFALLBACK_RUNTIME_PREFIX='"/usr"'
LDFLAGS = {ldfl}
CURL_CFLAGS = -I/usr/include
CURL_LDFLAGS = -lcurl -lbearssl -lz -lm -ldl -lpthread
USE_CURL_FOR_IMAP_SEND = Yes
NO_OPENSSL = Yes
NO_GETTEXT = Yes
NO_PERL = Yes
NO_PYTHON = Yes
NO_TCLTK = Yes
NO_INSTALL_HARDLINKS = Yes
NO_RUST = Yes
NO_REGEX = Yes
NO_EXPAT = Yes
"""
        )


def build(self):
    self.do(self.make_cmd, f"-j{self.make_jobs}", "all")


def install(self):
    self.do(
        self.make_cmd,
        "install",
        f"DESTDIR={self.chroot_destdir}",
    )

    # Match Oasis's trim: no Perl helpers, cvs/svn/p4 bridges, or scalar
    for cmd in ["git-cvsserver", "scalar"]:
        self.uninstall(f"cmd:{cmd}", missing_ok=True)
    for helper in [
        "git-archimport",
        "git-cvsexportcommit",
        "git-cvsimport",
        "git-cvsserver",
        "git-instaweb",
        "git-p4",
        "git-send-email",
        "git-svn",
    ]:
        self.uninstall(f"usr/lib/git-core/{helper}", missing_ok=True)

    # Prebuilt pages from the git-manpages tarball (the Oasis approach)
    skip = {
        "git-archimport.1",
        "git-cvsexportcommit.1",
        "git-cvsimport.1",
        "git-cvsserver.1",
        "git-instaweb.1",
        "git-p4.1",
        "git-send-email.1",
        "git-svn.1",
        "scalar.1",
    }
    for sec in (self.cwd / "man").glob("man*"):
        for page in sec.iterdir():
            if page.name not in skip:
                self.install_man(page)

    self.install_license("COPYING")
