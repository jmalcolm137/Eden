pkgname = "mkinitcpio"
pkgver = "42.2"
pkgrel = 0
build_style = "meson"
configure_args = [
    "-Ddocs=false",
    "-Dsystemd=disabled",
    "-Dsystemd_hooks=false",
    "-Dkernel_install=false",
    "-Dalpm=false",
]
hostmakedepends = ["muon"]
depends = [
    "bash",
    "kmod",
    "openbsd",
    "uutils-coreutils",
    "uutils-findutils",
    "xz",
    "zstd",
]
pkgdesc = "Arch-style initramfs generator"
license = "GPL-2.0-only"
url = "https://gitlab.archlinux.org/archlinux/mkinitcpio"
source = f"https://github.com/archlinux/mkinitcpio/archive/refs/tags/v{pkgver}.tar.gz"
sha256 = "0b79a89f9bf768f7413c55f8f09d9ec0efd77e312811935fe6a6ef06aadf3e0b"
# tests need a full Arch runtime
options = ["!check", "etcfiles"]


def prepare(self):
    # the release tarball has no git metadata for dist.sh
    m = self.cwd / "meson.build"
    text = m.read_text()
    text = text.replace(
        "version: run_command('tools/dist.sh', 'get-version', check: true).stdout().strip(),",
        f"version: '{pkgver}',",
    )
    out = []
    for line in text.splitlines():
        if line.startswith("udevd = find_program("):
            continue
        if line.startswith("tmpfiles = find_program("):
            continue
        if line.startswith("subdir('test')"):
            continue
        if line.startswith(("subdir('systemd')", "subdir('udev')", "subdir('tmpfiles')", "subdir('kernel-install')", "subdir('libalpm')", "subdir('man')")):
            continue
        if line.startswith("conf_data.set('UDEVD_PATH'"):
            line = "conf_data.set('UDEVD_PATH', '/usr/bin/udevd')"
        out.append(line)
    text = "\n".join(out) + "\n"
    m.write_text(text)


def post_install(self):
    self.install_license("LICENSE")
