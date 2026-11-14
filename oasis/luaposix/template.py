pkgname = "luaposix"
pkgver = "36.2.1"
pkgrel = 0
# Oasis pkg/luaposix/src
_commit = "5a8d8c768fc3c51f42cb591e9523a60399efc6a1"
makedepends = ["linux-headers", "lua"]
pkgdesc = "POSIX bindings for Lua"
license = "MIT"
url = "https://github.com/luaposix/luaposix"
source = f"{url}/archive/{_commit}.tar.gz"
sha256 = "afa1c8ce7e1686113b3dbeae2075ee94104649f7c5c4fc83ed493987c3990757"
# static-only module, as in the Oasis recipe
options = ["!lto", "!check"]

_cflags = ["-std=gnu99", "-D_GNU_SOURCE", "-include", "config.h", "-I.", "-Iext/include"]

_sources = [
    "ext/posix/ctype.c",
    "ext/posix/dirent.c",
    "ext/posix/errno.c",
    "ext/posix/fcntl.c",
    "ext/posix/fnmatch.c",
    "ext/posix/glob.c",
    "ext/posix/grp.c",
    "ext/posix/libgen.c",
    "ext/posix/poll.c",
    "ext/posix/pwd.c",
    "ext/posix/sched.c",
    "ext/posix/signal.c",
    "ext/posix/stdio.c",
    "ext/posix/stdlib.c",
    "ext/posix/sys/msg.c",
    "ext/posix/sys/resource.c",
    "ext/posix/sys/socket.c",
    "ext/posix/sys/stat.c",
    "ext/posix/sys/statvfs.c",
    "ext/posix/sys/time.c",
    "ext/posix/sys/times.c",
    "ext/posix/sys/utsname.c",
    "ext/posix/sys/wait.c",
    "ext/posix/syslog.c",
    "ext/posix/termio.c",
    "ext/posix/time.c",
    "ext/posix/unistd.c",
    "ext/posix/utime.c",
]

_lua_files = [
    "init.lua",
    "_base.lua",
    "_bitwise.lua",
    "_strict.lua",
    "compat.lua",
    "sys.lua",
    "util.lua",
]


def pre_build(self):
    self.cp(self.files_path / "config.h", "config.h")


def build(self):
    from cbuild.util import compiler

    cc = compiler.C(self)
    self.mkdir("obj", parents=True)
    objs = []
    for src in _sources:
        obj = "obj/" + src.replace("/", "_").removesuffix(".c") + ".o"
        cc.invoke([src], obj, obj_file=True, flags=_cflags)
        objs.append(obj)
    self.do("ar", "rcs", "libluaposix.a", *objs)


def install(self):
    self.install_lib("libluaposix.a", mode=0o644)
    for name in _lua_files:
        self.install_file(f"lib/posix/{name}", "usr/share/lua/5.5/posix")
    version = (self.cwd / "lib/posix/version.lua.in").read_text()
    version = version.replace("@package@", "luaposix").replace("@version2", "36.2.1")
    self.install_dir("usr/share/lua/5.5/posix")
    (self.destdir / "usr/share/lua/5.5/posix/version.lua").write_text(version)
    self.install_license("LICENSE")
