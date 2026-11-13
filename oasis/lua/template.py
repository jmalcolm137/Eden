pkgname = "lua"
pkgver = "5.5.0"
pkgrel = 0
build_style = "makefile"
make_build_target = "posix"
pkgdesc = "Lua scripting language from Oasis"
license = "MIT"
url = "https://www.lua.org"
# lua.org is frequently unavailable; use a mirror of the same tarball
source = f"https://download.automotivelinux.org/AGL/mirror/lua-{pkgver}.tar.gz"
sha256 = "57ccc32bbbd005cab75bcc52444052535af691789dba2b9016d5c50640d68b3d"
# upstream has no real test suite in the source tarball
# static library is installed in the main package, like Oasis does
options = ["!check", "!lto"]


def init_configure(self):
    self.make_install_args += [
        "INSTALL=install",
        "INSTALL_TOP=" + str(self.chroot_destdir / "usr"),
        "INSTALL_MAN=" + str(self.chroot_destdir / "usr/share/man/man1"),
    ]


def build(self):
    # Lua's makefile expects the archive operation in AR, so avoid the
    # generic makefile build that would pass plain AR=ar.
    self.do(
        self.make_cmd,
        f"-j{self.make_jobs}",
        "posix",
        "AR=ar rcu",
        "RANLIB=" + self.get_tool("RANLIB"),
        "CC=" + self.get_tool("CC"),
        "CFLAGS=" + self.get_cflags(shell=True),
        "LDFLAGS=" + self.get_ldflags(shell=True),
    )


def post_install(self):
    self.install_file(self.files_path / "lua.pc", "usr/lib/pkgconfig")
    self.install_license("doc/readme.html")
