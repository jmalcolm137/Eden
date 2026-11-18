pkgname = "sqlite"
pkgver = "3.54.1"
pkgrel = 1
build_style = "gnu_configure"
configure_args = ["--enable-threadsafe"]
configure_gen = []
hostmakedepends = ["pkgconf"]
pkgdesc = "Embedded SQL database engine"
license = "custom:public-domain"
url = "https://sqlite.org"
source = "https://www.sqlite.org/2026/sqlite-autoconf-3540100.tar.gz"
sha256 = "926ef8d3eab93fbf6e06011901273eec076b25594a4e1cdadd50c987f4f6d64e"
# tests are part of the upstream tree and not needed
skip_providers = ["usr/lib/libsqlite3.so.3.54.1"]
# tests are part of the upstream tree and not needed
options = ["!check", "!distlicense"]


@subpackage("sqlite-devel")
def _(self):
    return self.default_devel()


def init_build(self):
    self.make_build_env = dict(self.make_build_env or {})
    self.make_build_env["LDFLAGS"] = (
        " ".join(self.get_ldflags()) + " -Wl,-soname,libsqlite3.so.0"
    )
