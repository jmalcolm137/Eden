pkgname = "util-linux"
pkgver = "2.41.3"
pkgrel = 0
build_style = "gnu_configure"
configure_args = [
    "--disable-liblastlog2",
    "--disable-su",
    "--disable-runuser",
    "--disable-bash-completion",
    "--disable-makeinstall-chown",
    "--without-systemd",
    "--without-udev",
    "--without-ncursesw",
    "--without-ncurses",
]
configure_gen = []
makedepends = ["linux-headers"]
pkgdesc = "Miscellaneous system utilities"
license = "GPL-2.0-or-later AND LGPL-2.1-or-later AND BSD-3-Clause"
url = "https://www.kernel.org/pub/linux/utils/util-linux"
source = f"{url}/v2.41/util-linux-{pkgver}.tar.gz"
sha256 = "24160e7c3bfc6feecb9076706437fdb1212817549aaf9b4408f5a8e0b94e3eca"
# no test suite in the Oasis recipe
options = ["!check"]


def pre_build(self):
    for name, var in (
        ("all_errnos", "ERRNO_INCLUDES"),
        ("all_syscalls", "SYSCALL_INCLUDES"),
    ):
        p = self.cwd / "tools" / name
        text = p.read_text()
        text = text.replace("#!/bin/bash", "#!/bin/sh")
        text = text.replace("set -o pipefail\n", "")
        old = f'"$@" -MD -MF "$OUTPUT.deps" <<< "${var}"'
        new = f'printf \'%s\\n\' "${var}" | "$@" -MD -MF "$OUTPUT.deps"'
        text = text.replace(old, new)
        p.write_text(text)


def post_install(self):
    self.install_license("COPYING")
    sbin = self.destdir / "usr/sbin"
    if sbin.is_dir():
        bindir = self.destdir / "usr/bin"
        for f in sbin.iterdir():
            f.rename(bindir / f.name)
        sbin.rmdir()
    for name in ("mount", "umount"):
        p = self.destdir / "usr/bin" / name
        if p.exists():
            p.chmod(0o755)


@subpackage("util-linux-devel")
def _(self):
    return self.default_devel()
