pkgname = "base-files"
pkgver = "1.0"
pkgrel = 1
pkgdesc = "Minimal base filesystem and account files for the bldroot"
license = "custom:meta"
url = "https://oasislinux.org"
# no tests; this only installs filesystem skeleton and account files
options = ["etcfiles", "!check", "bootstrap", "keepempty", "brokenlinks"]


def install(self):
    for d in [
        "boot",
        "dev",
        "etc",
        "home",
        "media",
        "mnt",
        "proc",
        "root",
        "run",
        "sys",
        "tmp",
        "usr",
        "var",
    ]:
        self.install_dir(d)

    for d in ["bin", "include", "lib", "libexec", "share", "src"]:
        self.install_dir("usr/" + d)

    for d in ["log", "tmp"]:
        self.install_dir("var/" + d)

    self.install_dir("etc/ssl/certs")
    self.install_dir("etc/ssl/private")
    self.install_link(
        "etc/ca-certificates.conf",
        "../usr/share/ca-certificates/ca-certificates.conf",
    )
    # Usually created by ca-certificates' sd-tmpfiles entry; we don't ship
    # sd-tools in the minimal bldroot, so provide the path directly.
    self.install_link("etc/ssl/certs.pem", "certs/ca-certificates.crt")

    for d in ["bin", "lib"]:
        self.install_link(d, "usr/" + d)

    self.install_link("sbin", "usr/bin")
    self.install_link("usr/sbin", "bin")

    # empty drop-in directory for GNU tool compatibility entries; packages
    # install their alternative binaries here and users prepend it to PATH
    self.install_dir("usr/bin/gnu")

    libwn = f"lib{self.profile.wordsize}"
    self.install_link(libwn, "lib")
    self.install_link(f"usr/{libwn}", "lib")

    self.install_file(self.files_path / "etc/passwd", "etc")
    self.install_file(self.files_path / "etc/group", "etc")

    (self.destdir / "root").chmod(0o750)
    (self.destdir / "tmp").chmod(0o1777)
    (self.destdir / "var/tmp").chmod(0o1777)
