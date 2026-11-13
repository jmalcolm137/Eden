pkgname = "wayland"
pkgver = "1.21.0"
pkgrel = 0
# Oasis pkg/wayland/src
_commit = "8135e856ebd79872f886466e9cee39affb7d9ee8"
makedepends = ["expat", "libffi"]
pkgdesc = "Wayland compositor infrastructure from Oasis"
license = "MIT"
url = "https://wayland.freedesktop.org"
source = f"https://github.com/wayland-mirror/wayland/archive/{_commit}.tar.gz"
sha256 = "b1cc838bd7afdf4817682cb17cb9a2ee1cf0b91fb74a10d43c23a06ded41d80e"
# no test suite
options = ["!check", "!lto"]

_client_sources = [
    "src/wayland-client.c",
]
_server_sources = [
    "src/wayland-server.c",
    "src/wayland-shm.c",
    "src/event-loop.c",
]


def pre_build(self):
    self.cp(self.files_path / "config.h", "config.h")
    for p in sorted(self.files_path.glob("0*.patch")):
        self.cp(p, p.name)
        self.do("patch", "-p1", "-i", p.name)

    text = (self.cwd / "src/wayland-version.h.in").read_text()
    text = text.replace("@WAYLAND_VERSION_MAJOR@", "1")
    text = text.replace("@WAYLAND_VERSION_MINOR@", "21")
    text = text.replace("@WAYLAND_VERSION_MICRO@", "0")
    text = text.replace("@WAYLAND_VERSION@", "1.21.0")
    self.mkdir("include", parents=True)
    (self.cwd / "include/wayland-version.h").write_text(text)


def build(self):
    from cbuild.util import compiler

    cc = compiler.C(self)
    flags = ["-DHAVE_CONFIG_H", "-I.", "-Iinclude", "-Isrc"]
    self.mkdir("obj", parents=True)

    common = []
    for src in ["src/wayland-util.c", "src/wayland-os.c", "src/connection.c"]:
        obj = "obj/" + src.replace("/", "_").removesuffix(".c") + ".o"
        cc.invoke([src], obj, obj_file=True, flags=flags)
        common.append(obj)

    cc.invoke(
        ["src/scanner.c", common[0]],
        "wayland-scanner",
        flags=flags,
        ldflags=["-lexpat"],
    )

    self.do(
        "./wayland-scanner", "client-header", "protocol/wayland.xml",
        "include/wayland-client-protocol.h",
    )
    self.do(
        "./wayland-scanner", "server-header", "protocol/wayland.xml",
        "include/wayland-server-protocol.h",
    )
    self.do(
        "./wayland-scanner", "private-code", "protocol/wayland.xml",
        "src/wayland-protocol.c",
    )

    proto = "obj/wayland-protocol.o"
    cc.invoke(["src/wayland-protocol.c"], proto, obj_file=True, flags=flags)

    server_objs = list(common)
    for src in _server_sources:
        obj = "obj/" + src.replace("/", "_").removesuffix(".c") + ".o"
        cc.invoke([src], obj, obj_file=True, flags=flags)
        server_objs.append(obj)
    server_objs.append(proto)
    self.do("ar", "rcs", "libwayland-server.a", *server_objs)

    client_objs = [common[0], common[1], common[2], proto]
    for src in _client_sources:
        obj = "obj/" + src.replace("/", "_").removesuffix(".c") + ".o"
        cc.invoke([src], obj, obj_file=True, flags=flags)
        client_objs.append(obj)
    self.do("ar", "rcs", "libwayland-client.a", *client_objs)

    cursor_objs = []
    for src in [
        "cursor/os-compatibility.c",
        "cursor/wayland-cursor.c",
        "cursor/xcursor.c",
    ]:
        obj = "obj/" + src.replace("/", "_").removesuffix(".c") + ".o"
        cc.invoke([src], obj, obj_file=True, flags=flags)
        cursor_objs.append(obj)
    self.do("ar", "rcs", "libwayland-cursor.a", *cursor_objs)


def install(self):
    self.install_file("wayland-scanner", "usr/bin", mode=0o755)
    self.install_file("libwayland-client.a", "usr/lib")
    self.install_file("libwayland-server.a", "usr/lib")
    self.install_file("libwayland-cursor.a", "usr/lib")

    for h in [
        "wayland-client-core.h",
        "wayland-client.h",
        "wayland-server-core.h",
        "wayland-server.h",
        "wayland-util.h",
    ]:
        self.install_file(f"src/{h}", "usr/include")
    self.install_file("cursor/wayland-cursor.h", "usr/include")
    for h in [
        "wayland-client-protocol.h",
        "wayland-server-protocol.h",
        "wayland-version.h",
    ]:
        self.install_file(f"include/{h}", "usr/include")
    self.install_license("COPYING")
