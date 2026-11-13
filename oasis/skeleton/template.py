pkgname = "skeleton"
pkgver = "1.0"
pkgrel = 0
pkgdesc = "Oasis filesystem skeleton"
license = "custom:meta"
url = "https://oasislinux.org"
# installs the Oasis root filesystem layout
options = ["etcfiles", "!check", "keepempty", "brokenlinks"]


def pre_build(self):
    self.cp(self.files_path / "applyperms.c", "applyperms.c")
    self.cp(self.files_path / "mergeperms.c", "mergeperms.c")


def build(self):
    from cbuild.util import compiler

    cc = compiler.C(self)
    cc.invoke(["applyperms.c"], "applyperms", flags=["-std=c99", "-Wall"])
    cc.invoke(["mergeperms.c"], "mergeperms", flags=["-std=c99", "-Wall"])


def install(self):
    for d in [
        "bin",
        "boot",
        "dev",
        "etc",
        "home",
        "mnt",
        "proc",
        "root",
        "run",
        "sys",
        "tmp",
        "var",
        "var/db",
        "var/empty",
        "var/log",
    ]:
        self.install_dir(d)

    self.install_dir("root", mode=0o700)
    self.install_dir("usr")
    self.install_link("usr/bin", "../bin")
    self.install_link("bin/plumb", "../etc/plumb")

    self.install_file(self.files_path / "gitignore", ".", name=".gitignore")
    self.install_file("applyperms", "usr/libexec", mode=0o755)
    self.install_file("mergeperms", "usr/libexec", mode=0o755)
