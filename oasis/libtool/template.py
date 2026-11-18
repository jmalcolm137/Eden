pkgname = "libtool"
pkgver = "2.5.4"
pkgrel = 5
build_style = "gnu_configure"
configure_gen = []
hostmakedepends = [
    "automake",
    "m4",
    "perl",
]
depends = ["m4", "cmd:tar!base-files"]
pkgdesc = "Generic library support script"
license = "GPL-2.0-or-later AND LGPL-2.0-or-later"
url = "https://www.gnu.org/software/libtool"
source = f"https://ftp.gnu.org/gnu/libtool/libtool-{pkgver}.tar.gz"
sha256 = "da8ebb2ce4dcf46b90098daf962cffa68f4b4f62ea60f798d0ef12929ede6adf"
# FIXME: need to clear out sysroot from usr/bin/libtool for cross
# also keep libtool static compat intact
# tests interminable and endless
options = ["!check", "!cross", "!lto"]


@subpackage("libtool-devel")
def _(self):
    # transitional
    self.provides = [self.with_pkgver("libltdl-devel")]
    # can't use default_devel, some aclocal stuff belongs in main package
    return [
        "usr/include",
        "usr/lib/*.so",
        "usr/lib/*.a",
        "usr/share/aclocal/ltdl.m4",
        "usr/share/libtool/libltdl",
    ]


@subpackage("libtool-libs")
def _(self):
    # transitional
    self.provides = [self.with_pkgver("libltdl")]

    return self.default_libs()


def pre_build(self):
    for f in ("doc/libtool.1", "doc/libtoolize.1", "doc/libtool.info"):
        (self.cwd / f).touch()
    stub = self.cwd / "help2man"
    stub.write_text(
        "#!/bin/sh\n"
        "out=\n"
        "prev=\n"
        "for a in \"$@\"; do\n"
        "  case \"$a\" in --output=*) out=\"${a#--output=}\" ;; esac\n"
        "  [ \"$prev\" = \"--output\" ] && out=\"$a\"\n"
        "  prev=\"$a\"\n"
        "done\n"
        "[ -n \"$out\" ] && : > \"$out\"\n"
        "exit 0\n"
    )
    stub.chmod(0o755)
    self.make_build_env = dict(self.make_build_env or {})
    self.make_build_env["PATH"] = str(self.chroot_cwd) + ":" + self.make_build_env.get("PATH", "/usr/bin:/bin")
