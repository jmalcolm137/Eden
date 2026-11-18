pkgname = "openbsd"
pkgver = "8.0"
pkgrel = 1
makedepends = [
    "bearssl-devel-static", "byacc", "libatomic-chimera-devel-static",
    "libtls-bearssl-devel-static", "linux-headers", "musl-bsd-headers",
    "musl-devel-static",
]
provides = ["m4"]
triggers = ["/usr/bin/doas"]
pkgdesc = "OpenBSD libc compatibility library and tools"
license = "ISC"
url = "https://www.openbsd.org"
source = [
    "https://cloudflare.cdn.openbsd.org/pub/OpenBSD/8.0/src.tar.gz",
    "https://cloudflare.cdn.openbsd.org/pub/OpenBSD/8.0/sys.tar.gz",
]
sha256 = [
    "9984c74ff875b5ff041e4676a7f3e4e1ead2cc47a284d705eb9f37cbec4fe795",
    "964b1aed7839b86f4e010a0fdd03dcd409e6f569e69fe85f95e5fceb740c2aaf",
]
tool_flags = {"LDFLAGS": ["-static-pie", "-unwindlib=none"]}
file_modes = {"usr/bin/doas": ("root", "root", 0o6755)}
# only the subset used by the Oasis tree is built
options = ["!check"]

_cflags = [
    "-std=gnu17", "-Wall", "-Wno-pointer-sign", "-Wno-maybe-uninitialized",
    "-Wno-attributes", '-DDEF_WEAK(n)=_Static_assert(1, "")',
    "-Iobsd-include",
]

_libbsd = [
    "lib/libc/crypt/arc4random_uniform.c",
    "lib/libc/gen/fts.c",
    "lib/libc/gen/getprogname.c",
    "lib/libc/gen/pwcache.c",
    "lib/libc/gen/readpassphrase.c",
    "lib/libc/gen/setprogname.c",
    "lib/libc/gen/unvis.c",
    "lib/libc/gen/vis.c",
    "lib/libc/gen/warnc.c",
    "lib/libc/gen/vwarnc.c",
    "lib/libc/net/base64.c",
    "lib/libc/stdlib/freezero.c",
    "lib/libc/stdlib/recallocarray.c",
    "lib/libc/stdlib/strtonum.c",
    "lib/libc/string/strmode.c",
    "lib/libc/string/timingsafe_bcmp.c",
    "lib/libc/string/timingsafe_memcmp.c",
    "lib/libutil/fmt_scaled.c",
    "lib/libutil/ohash.c",
]


def pre_build(self):
    self.mkdir("obsd-include/sys", parents=True)
    # compatibility shims
    shimroot = self.files_path / "include"
    for p in shimroot.rglob("*"):
        if not p.is_file():
            continue
        rel = p.relative_to(shimroot)
        (self.cwd / "obsd-include" / rel).parent.mkdir(parents=True, exist_ok=True)
        self.cp(p, self.cwd / "obsd-include" / rel)
    # upstream headers
    for src, dst in [
        ("sys/sys/queue.h", "obsd-include/sys/queue.h"),
        ("sys/sys/tree.h", "obsd-include/sys/tree.h"),
        ("sys/sys/_null.h", "obsd-include/sys/_null.h"),
        ("include/fts.h", "obsd-include/fts.h"),
        ("include/vis.h", "obsd-include/vis.h"),
        ("lib/libutil/ohash.h", "obsd-include/ohash.h"),
    ]:
        self.cp(self.cwd / src, self.cwd / dst)
    # use the Linux portability header for arc4random
    self.mkdir("arc4random", parents=True)
    self.cp(
        self.cwd / "lib/libc/crypt/arc4random.c",
        self.cwd / "arc4random/arc4random.c",
    )
    self.cp(
        self.cwd / "lib/libcrypto/arc4random/arc4random_linux.h",
        self.cwd / "arc4random/arc4random.h",
    )
    self.cp(
        self.cwd / "lib/libc/crypt/chacha_private.h",
        self.cwd / "arc4random/chacha_private.h",
    )


def build(self):
    from cbuild.util import compiler

    cc = compiler.C(self)
    self.mkdir("obj", parents=True)
    objs = []
    for src in _libbsd + ["arc4random/arc4random.c"]:
        obj = "obj/" + src.replace("/", "_") + ".o"
        cc.invoke([src], obj, obj_file=True, flags=_cflags)
        objs.append(obj)
    self.do("ar", "rcs", "libbsd.a", *objs)

    def exe(name, srcs, flags=None):
        cc.invoke(srcs + ["libbsd.a"], name, flags=_cflags + (flags or []))

    exe("diff", [
        "usr.bin/diff/diff.c", "usr.bin/diff/diffdir.c",
        "usr.bin/diff/diffreg.c", "usr.bin/diff/xmalloc.c",
    ])
    exe("fmt", ["usr.bin/fmt/fmt.c"])

    # doas
    self.mkdir("outdir/usr.bin/doas", parents=True)
    self.do(
        "byacc", "-d", "-o", "outdir/usr.bin/doas/parse.tab.c",
        "usr.bin/doas/parse.y",
    )
    exe("doas", [
        "usr.bin/doas/doas.c", "usr.bin/doas/env.c",
        "outdir/usr.bin/doas/parse.tab.c", "usr.bin/doas/persist.c",
    ], ["-D_GNU_SOURCE", "-Iusr.bin/doas"])

    # m4
    self.mkdir("outdir/usr.bin/m4", parents=True)
    self.do(
        "byacc", "-d", "-o", "outdir/usr.bin/m4/parser.tab.c",
        "usr.bin/m4/parser.y",
    )
    exe("m4", [
        "usr.bin/m4/eval.c", "usr.bin/m4/expr.c", "usr.bin/m4/look.c",
        "usr.bin/m4/main.c", "usr.bin/m4/misc.c", "usr.bin/m4/gnum4.c",
        "usr.bin/m4/trace.c", "usr.bin/m4/tokenizer.c",
        "outdir/usr.bin/m4/parser.tab.c",
    ], ["-Ioutdir/usr.bin/m4"])

    exe("patch", [
        "usr.bin/patch/patch.c", "usr.bin/patch/pch.c", "usr.bin/patch/inp.c",
        "usr.bin/patch/util.c", "usr.bin/patch/backupfile.c",
        "usr.bin/patch/mkpath.c", "usr.bin/patch/ed.c",
    ])

    exe("pax", [
        "bin/pax/ar_io.c", "bin/pax/ar_subs.c", "bin/pax/buf_subs.c",
        "bin/pax/cpio.c", "bin/pax/file_subs.c", "bin/pax/ftree.c",
        "bin/pax/gen_subs.c", "bin/pax/getoldopt.c", "bin/pax/options.c",
        "bin/pax/pat_rep.c", "bin/pax/pax.c", "bin/pax/sel_subs.c",
        "bin/pax/tables.c", "bin/pax/tar.c", "bin/pax/tty_subs.c",
    ], ["-D_GNU_SOURCE"])

    exe("rsync", [
        "usr.bin/rsync/blocks.c", "usr.bin/rsync/client.c",
        "usr.bin/rsync/copy.c", "usr.bin/rsync/downloader.c",
        "usr.bin/rsync/fargs.c", "usr.bin/rsync/flist.c",
        "usr.bin/rsync/hash.c", "usr.bin/rsync/ids.c", "usr.bin/rsync/io.c",
        "usr.bin/rsync/log.c", "usr.bin/rsync/main.c", "usr.bin/rsync/md4.c",
        "usr.bin/rsync/misc.c", "usr.bin/rsync/mkpath.c",
        "usr.bin/rsync/mktemp.c", "usr.bin/rsync/receiver.c",
        "usr.bin/rsync/rmatch.c", "usr.bin/rsync/rules.c",
        "usr.bin/rsync/sender.c", "usr.bin/rsync/server.c",
        "usr.bin/rsync/session.c", "usr.bin/rsync/socket.c",
        "usr.bin/rsync/symlinks.c", "usr.bin/rsync/uploader.c",
    ], ["-D_GNU_SOURCE"])

    cc.invoke([
        "usr.bin/nc/netcat.c", "usr.bin/nc/atomicio.c",
        "usr.bin/nc/socks.c", "/usr/lib/libtls.a", "/usr/lib/libbearssl.a",
        "-lpthread", "libbsd.a",
    ], "nc", flags=_cflags + ["-D_GNU_SOURCE"])


def install(self):
    self.install_lib("libbsd.a")
    for bin in ("diff", "fmt", "doas", "m4", "patch", "rsync", "nc"):
        self.install_bin(bin, mode=0o6755 if bin == "doas" else 0o755)
    self.install_bin("pax", name="tar")
    self.install_link("usr/bin/cpio", "tar")
    for man in [
        "usr.bin/diff/diff.1", "usr.bin/doas/doas.1",
        "usr.bin/doas/doas.conf.5", "usr.bin/fmt/fmt.1", "usr.bin/m4/m4.1",
        "usr.bin/patch/patch.1", "bin/pax/tar.1", "bin/pax/cpio.1",
        "usr.bin/rsync/rsync.1", "usr.bin/rsync/rsync.5",
        "usr.bin/rsync/rsyncd.5", "usr.bin/nc/nc.1",
    ]:
        self.install_man(man)
    shimroot = self.files_path / "include"
    for p in shimroot.rglob("*"):
        if not p.is_file():
            continue
        rel = p.relative_to(shimroot)
        self.install_file(p, f"usr/include/openbsd/{rel.parent}")
    for src in ["include/fts.h", "include/vis.h", "lib/libutil/ohash.h"]:
        self.install_file(src, "usr/include/openbsd")
    for src in ["sys/sys/queue.h", "sys/sys/tree.h", "sys/sys/_null.h"]:
        self.install_file(src, "usr/include/openbsd/sys")
    self.install_license(self.files_path / "LICENSE")


@subpackage("openbsd-devel")
def _(self):
    return self.default_devel()
