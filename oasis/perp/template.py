pkgname = "perp"
pkgver = "2.07"
pkgrel = 0
pkgdesc = "Persistent process supervision suite from Oasis"
license = "custom:perp"
url = "http://b0llix.net/perp"
source = f"{url}/distfiles/perp-{pkgver}.tar.gz"
sha256 = "1222fe31c16014d8b2a78416f93ba9f8c31eddbc381adc9021fa5d9764475815"
# upstream has no test suite
options = ["!check"]

_perp_cmds = [
    "perpd",
    "perpboot",
    "perpctl",
    "perphup",
    "perpls",
    "perpok",
    "perpstat",
    "tinylog",
]

_runtools = [
    "runargs",
    "runargv0",
    "runchoom",
    "rundetach",
    "rundeux",
    "runenv",
    "runfile",
    "runlimit",
    "runlock",
    "runpause",
    "runsession",
    "runtool",
    "runtrap",
    "runuid",
]

_cattools = ["catargs", "catenv", "catlimits", "catuid"]

_perp_mans = [
    "perpd.8",
    "perpboot.8",
    "perpctl.8",
    "perphup.8",
    "perpls.8",
    "perpok.8",
    "perpstat.8",
    "tinylog.8",
    "perpetrate.5",
    "perp_intro.8",
]


def build(self):
    cflags = " ".join([
        self.get_cflags(shell=True),
        "-std=c99",
        "-Wall",
        "-Wpedantic",
        "-Wno-array-parameter",
        "-Wno-misleading-indentation",
        "-D_GNU_SOURCE",
        "-DNDEBUG",
        '-DTINYLOG_ZIP=\\"/bin/gzip\\"',
        '-DZIP_EXT=\\".gz\\"',
        "-I.",
        "-I../lasagna",
    ])
    ldflags = " ".join([
        self.get_ldflags(shell=True),
        "-L../lasagna",
        "-lasagna",
    ])
    args = [
        "CC=" + self.get_tool("CC"),
        "CFLAGS=" + cflags,
        "LDFLAGS=" + ldflags,
    ]
    jobs = f"-j{self.make_jobs}"

    self.do(self.make_cmd, jobs, "-C", "lasagna", *args)
    self.do(
        self.make_cmd,
        jobs,
        "-C",
        "perp",
        *_perp_cmds,
        *args,
    )
    self.do(self.make_cmd, jobs, "-C", "runtools", "all", *args)


def install(self):
    for cmd in _perp_cmds:
        self.install_bin(f"perp/{cmd}")
    for tool in _runtools + _cattools:
        self.install_bin(f"runtools/{tool}")

    for man in _perp_mans:
        self.install_man(f"perp/man/{man}")
    for tool in _runtools:
        self.install_man(f"runtools/man/{tool}.8")
    self.install_man("runtools/man/runtools_intro.8")

    self.install_license("LICENSE")
