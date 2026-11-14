pkgname = "blind"
pkgver = "1.1"
pkgrel = 4
pkgdesc = "Collection of image processing tools"
license = "ISC"
url = "https://tools.suckless.org/blind"
# source is the Oasis-pinned suckless commit, vendored under files/
options = ["!check"]

_cflags = [
    "-std=c99", "-Wall", "-Wpedantic",
    "-D_DEFAULT_SOURCE", "-DHAVE_PRCTL", "-DHAVE_EPOLL",
]

_scripts = ["blind-rotate-90", "blind-rotate-180", "blind-rotate-270"]


def pre_build(self):
    self.cp(self.files_path / "src", "src", recursive=True)
    self.cp(self.files_path / "man", "man", recursive=True)
    for name in _scripts + ["LICENSE"]:
        self.cp(self.files_path / name, name)


def build(self):
    from cbuild.util import compiler

    cc = compiler.C(self)
    self.mkdir("obj", parents=True)
    self.mkdir("bin", parents=True)
    util_objs = []
    for src in ("src/util.c", "src/stream.c"):
        obj = "obj/" + src.replace("/", "_").removesuffix(".c") + ".o"
        cc.invoke([src], obj, obj_file=True, flags=_cflags)
        util_objs.append(obj)
    self.do("ar", "rcs", "libutil.a", *util_objs)

    for src in sorted((self.cwd / "src").glob("blind-*.c")):
        name = src.stem
        cc.invoke([f"src/{src.name}", "libutil.a"], f"bin/{name}", flags=_cflags)


def install(self):
    for src in sorted((self.cwd / "src").glob("blind-*.c")):
        self.install_bin(f"bin/{src.stem}", name=src.stem)
    for name in _scripts + ["LICENSE"]:
        self.install_bin(name)
    self.install_man("man/*.1", glob=True)
    self.install_man("man/blind.7")
    self.install_license("LICENSE")
