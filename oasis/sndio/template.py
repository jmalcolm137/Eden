pkgname = "sndio"
pkgver = "1.9.0"
pkgrel = 1
# Oasis pkg/sndio/src
_commit = "584d41515a981818f6f60e9d9dca97af3657a640"
makedepends = [
    "linux-headers",
    "tinyalsa-devel",
    "tinyalsa-devel-static",
]
pkgdesc = "Small audio and MIDI framework"
license = "ISC"
url = "https://sndio.org"
source = f"https://github.com/ratchov/sndio/archive/{_commit}.tar.gz"
sha256 = "dbcffafbf2934c57047243812a319853c75f450dcf390f6a32ab596854de5c39"
# no test suite in the Oasis recipe
options = ["!check"]

_cflags = [
    "-std=c99",
    "-Wall",
    "-Wpedantic",
    "-Wno-format-truncation",
    "-Wno-maybe-uninitialized",
    "-D_GNU_SOURCE",
    "-Ilibsndio",
    "-Ibsd-compat",
    "-include",
    "config.h",
]

_lib_sources = [
    "libsndio/debug.c",
    "libsndio/aucat.c",
    "libsndio/mio.c",
    "libsndio/mio_aucat.c",
    "libsndio/sio_aucat.c",
    "libsndio/sioctl.c",
    "libsndio/sioctl_aucat.c",
    "bsd-compat/getpeereid.c",
    "bsd-compat/issetugid.c",
    "bsd-compat/strlcat.c",
    "bsd-compat/strlcpy.c",
    "bsd-compat/strtonum.c",
    "bsd-compat/clock_gettime.c",
    "libsndio/sio.c",
]

_sndiod_sources = [
    "sndiod/abuf.c",
    "sndiod/utils.c",
    "sndiod/dev.c",
    "sndiod/dev_sioctl.c",
    "sndiod/dsp.c",
    "sndiod/file.c",
    "sndiod/listen.c",
    "sndiod/midi.c",
    "sndiod/miofile.c",
    "sndiod/opt.c",
    "sndiod/siofile.c",
    "sndiod/sndiod.c",
    "sndiod/sock.c",
]

_aucat_sources = [
    "aucat/abuf.c",
    "aucat/afile.c",
    "aucat/aucat.c",
    "aucat/dsp.c",
    "aucat/utils.c",
]


def pre_build(self):
    self.cp(self.files_path / "config.h", "config.h")
    p = self.cwd / "libsndio/sio_alsa.c"
    text = p.read_text()
    text = text.replace(
        '#include "debug.h"',
        "int pcm_state(struct pcm *);\n\n#include \"debug.h\"",
    )
    p.write_text(text)



def build(self):
    from cbuild.util import compiler

    cc = compiler.C(self)
    self.mkdir("obj", parents=True)
    self.mkdir("out", parents=True)
    objs = []
    for src in _lib_sources:
        obj = "obj/" + src.replace("/", "_").removesuffix(".c") + ".o"
        cc.invoke([src], obj, obj_file=True, flags=_cflags)
        objs.append(obj)
    self.do("ar", "rcs", "libsndio.a", *objs)

    sobjs = []
    for src in _sndiod_sources:
        obj = "obj/" + src.replace("/", "_").removesuffix(".c") + ".o"
        cc.invoke([src], obj, obj_file=True, flags=_cflags)
        sobjs.append(obj)

    for src, obj in (
        ("libsndio/sio.c", "obj/sio.o"),
        ("libsndio/sio_alsa.c", "obj/sio_alsa.o"),
    ):
        cc.invoke([src], obj, obj_file=True, flags=[*_cflags, "-DUSE_ALSA"])
        sobjs.append(obj)

    cc.invoke(
        [*sobjs, "libsndio.a"],
        "out/sndiod",
        flags=_cflags,
        ldflags=["/usr/lib/libtinyalsa.a"],
    )
    cc.invoke(["sndioctl/sndioctl.c", "libsndio.a"], "out/sndioctl", flags=_cflags)
    cc.invoke([*_aucat_sources, "libsndio.a"], "out/aucat", flags=_cflags)


def install(self):
    self.install_bin("out/sndiod", name="sndiod")
    self.install_bin("out/sndioctl", name="sndioctl")
    self.install_bin("out/aucat", name="aucat")
    self.install_man("sndiod/sndiod.8")
    self.install_man("sndioctl/sndioctl.1")
    self.install_man("aucat/aucat.1")
    self.install_license(self.files_path / "LICENSE")
