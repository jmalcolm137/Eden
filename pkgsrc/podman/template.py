pkgname = "podman"
pkgver = "6.2.1"
pkgrel = 0
hostmakedepends = [
    "bash",
    "gmake",
    "go",
    "go-md2man",
    "mandoc",
    "perl",
    "python",
]
makedepends = ["libseccomp-devel", "linux-headers", "sqlite-devel"]
# a runtime and the container monitor are required to run containers
depends = ["aardvark-dns", "conmon", "crun", "netavark"]
pkgdesc = "Tool for managing OCI containers and pods"
license = "Apache-2.0"
url = "https://podman.io"
source = f"https://github.com/containers/podman/archive/refs/tags/v{pkgver}.tar.gz"
sha256 = "10a56f6a36c4f7ea19956d7298615a6ff1f46978fc36d31dfe31be14899d10fb"
# the test suite needs a privileged container environment
options = ["!check", "!lto", "etcfiles"]

# Everything the upstream Makefile would pick up automatically.  AppArmor,
# btrfs, devicemapper and the systemd/journald integration are left out
# (Eden uses perp and has none of those libraries), and OpenPGP is used
# instead of gpgme for image signatures.
_tags = [
    "containers_image_openpgp",
    "exclude_graphdriver_btrfs",
    "exclude_graphdriver_devicemapper",
    "libsqlite3",
    "seccomp",
]
# the remote client is built without the local storage/network backends
_remote_tags = ["containers_image_openpgp", "exclude_graphdriver_btrfs", "remote"]


def _env(self):
    from cbuild.util import golang

    env = golang.get_go_env(self)
    env.update(
        {
            "CGO_ENABLED": "1",
            "CC": "clang",
            "CXX": "clang++",
            "GOTOOLCHAIN": "local",
        }
    )
    return env


def _ldflags(self):
    return " ".join(
        [
            f"-X go.podman.io/podman/v6/libpod/define.buildInfo={self.source_date_epoch}",
            "-X go.podman.io/common/pkg/config._installPrefix=/usr",
            "-X go.podman.io/common/pkg/config._etcDir=/etc",
            "-X go.podman.io/common/pkg/config.additionalHelperBinariesDir=/usr/lib/podman",
        ]
    )


def build(self):
    env = _env(self)
    common = [
        "-v",
        "-trimpath",
        "-buildvcs=false",
        "-buildmode=pie",
        "-ldflags",
        _ldflags(self),
        "-mod=vendor",
    ]
    self.do(
        "go",
        "build",
        *common,
        "-tags",
        ",".join(_tags),
        "-o",
        "bin/podman",
        "./cmd/podman",
        env=env,
    )
    self.do(
        "go",
        "build",
        *common,
        "-tags",
        ",".join(_remote_tags),
        "-o",
        "bin/podman-remote",
        "./cmd/podman",
        env=env,
    )
    self.do(
        "go",
        "build",
        *common,
        "-o",
        "bin/rootlessport",
        "./cmd/rootlessport",
        env=env,
    )

    # generate the man pages and their aliases
    self.do("gmake", "docs", "GOMD2MAN=go-md2man", env=env)


def install(self):
    self.install_bin(self.cwd / "bin" / "podman")
    self.install_bin(self.cwd / "bin" / "podman-remote")
    self.install_file(self.cwd / "bin" / "rootlessport", "usr/lib/podman", 0o755)

    self.install_dir("usr/bin")
    self.install_link("usr/bin/podmansh", "podman")

    # default configuration; containers-common is not packaged
    self.install_file(self.files_path / "policy.json", "etc/containers")
    self.install_file(self.files_path / "registries.conf", "etc/containers")
    self.install_file(
        "vendor/go.podman.io/common/pkg/seccomp/seccomp.json",
        "usr/share/containers",
    )

    env = {"DESTDIR": self.chroot_destdir}
    self.do(
        "gmake",
        "install.man",
        "install.completions",
        "PREFIX=/usr",
        env=env,
    )

    self.install_license("LICENSE")
