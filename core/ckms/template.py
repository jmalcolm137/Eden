pkgname = "ckms"
pkgver = "0.1.1"
pkgrel = 0
build_style = "makefile"
hostmakedepends = []
depends = ["python"]
pkgdesc = "Chimera Kernel Module System"
license = "BSD-2-Clause"
url = "https://github.com/chimera-linux/ckms"
source = f"{url}/archive/refs/tags/v{pkgver}.tar.gz"
sha256 = "d15e252fc5a9fa6d9a9187979512849b1634a52c4b98d44839a3f42464964021"
# no tests
options = ["etcfiles", "!check"]

# scdoc is only needed for the man page; provide a no-op stand-in
def prepare(self):
    self.mkdir("toolbin", parents=True)
    p = self.cwd / "toolbin" / "scdoc"
    p.write_text("#!/bin/sh\nexit 0\n")
    p.chmod(0o755)
    self.make_env = {
        "PATH": str(self.chroot_cwd / "toolbin") + ":/usr/bin:/bin"
    }


def post_install(self):
    self.install_license("COPYING.md")
    self.install_sysusers(self.files_path / "sysusers.conf")
    self.install_tmpfiles(self.files_path / "tmpfiles.conf")
    self.install_file(self.files_path / "10-ckms.sh", "usr/lib/kernel.d", mode=0o755)
    self.install_file(self.files_path / "refresh-initramfs.sh", "etc/ckms", mode=0o755)
    self.install_file(self.files_path / "depmod.sh", "etc/ckms", mode=0o755)
