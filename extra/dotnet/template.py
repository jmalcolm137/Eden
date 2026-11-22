pkgname = "dotnet"
pkgver = "10.0.113"
pkgrel = 1
archs = ["x86_64"]
prepare_after_patch = True
_bootstrap = "10.0.113-r1"
_gccver = "15.2.0-r9"
hostmakedepends = [
    "bash",
    "cmake",
    "curl",
    "file",
    "git",
    "gmake",
    "grep",
    "gtar",
    "patchelf",
    "pigz",
    "python",
    "samurai",
    "uutils-findutils",
    "xz",
]
makedepends = [
    "brotli-devel",
    "icu-devel",
    "krb5-devel",
    "libucontext-devel",
    "libunwind-devel",
    "libxml2-devel",
    "linux-headers",
    "openssl",
    "zlib",
    "zstd-devel",
]
depends = ["ca-certificates", "icu", "krb5"]
pkgdesc = ".NET SDK and runtime"
license = "MIT"
url = "https://dotnet.microsoft.com"
source = [
    f"https://github.com/dotnet/dotnet/archive/refs/tags/v{pkgver}.tar.gz",
    f"https://dl-cdn.alpinelinux.org/alpine/edge/community/x86_64/dotnet10-stage0-bootstrap-{_bootstrap}.apk>bootstrap.tar.gz",
    f"https://dl-cdn.alpinelinux.org/alpine/edge/community/x86_64/dotnet10-stage0-artifacts-{_bootstrap}.apk>artifacts.tar.gz",
    f"https://dl-cdn.alpinelinux.org/alpine/edge/main/x86_64/libstdc%2B%2B-{_gccver}.apk>libstdcxx.tar.gz",
    f"https://dl-cdn.alpinelinux.org/alpine/edge/main/x86_64/libgcc-{_gccver}.apk>libgcc.tar.gz",
]
source_paths = [
    ".",
    "bootstrap-pkg",
    "artifacts-pkg",
    "libstdcxx-pkg",
    "libgcc-pkg",
]
sha256 = [
    "5c3a5dcc776c94d314853ccf24d3a2b5627f2249c7defb8a8f0cbade8ecd4631",
    "705de653d699d5c4253332017a118d5f77a0cb6b1f82354ca92d889e879155d8",
    "690644eea93dcb3b6aa9cf6a9e7fc79d504ba30c41fd30c79b718a0d697269f8",
    "adfebfc0c4b80c293be8cc802a7fb73d7f5854f01b47ff1f40282d18f255b357",
    "01c9609197de10519ceb204a09d1efa54baad145f65bf00ba0908086692ca3fe",
]
hardening = ["!int"]
# the full source-build test suite needs network access and a bootstrapped SDK
options = ["!check", "!cross", "!lto", "etcfiles"]

_sdkver = "10.0.113"
_sdkroot = "/usr/lib/dotnet"


def _fix_modes(self, root):
    exec_names = {
        "apphost",
        "createdump",
        "dnx",
        "dotnet",
        "ilc",
        "singlefilehost",
    }
    data_suffixes = {
        ".a",
        ".c",
        ".cmake",
        ".cpp",
        ".def",
        ".dll",
        ".h",
        ".in",
        ".json",
        ".m",
        ".o",
        ".orig",
        ".pdb",
        ".props",
        ".pubxml",
        ".targets",
        ".txt",
        ".xml",
    }

    for path in root.rglob("*"):
        if path.is_symlink() or not path.is_file():
            continue

        mode = path.stat().st_mode
        name = path.name

        if name in exec_names or (name.startswith("lib") and ".so" in name):
            path.chmod(mode | 0o111)
        elif name.endswith(".sh"):
            path.chmod(mode | 0o111)
        elif path.suffix in data_suffixes:
            path.chmod(mode & ~0o111)


def _check_no_gcc(self, root):
    script = f'''
bad=
for f in $(find "{root}" -type f); do
    if readelf -d "$f" 2>/dev/null | grep -qE 'libstdc\\+\\+\\.so\\.6|libgcc_s\\.so\\.1'; then
        bad="$bad $f"
    fi
done
if [ -n "$bad" ]; then
    echo "GCC runtime dependency found:$bad" >&2
    exit 1
fi
'''
    self.do("sh", "-c", script)


def _sdk_archive(self):
    base = self.cwd / "artifacts/assets/Release"
    matches = sorted(base.rglob("dotnet-sdk-*.tar.gz"))
    if not matches:
        self.error("source build produced no dotnet SDK archive", bt=True)
    return str(self.chroot_cwd / "artifacts/assets/Release" / matches[0].relative_to(base))


def post_patch(self):
    # Keep all private build state outside the VMR tree. The source-build
    # binary scanner walks the tree and would otherwise block on the .NET
    # diagnostic FIFOs/sockets created under TMPDIR.
    aux = self.statedir / "aux"
    auxc = self.chroot_statedir / "aux"

    for d in [
        "bootstrap",
        "artifacts",
        "gcc-libs",
        "tools",
        "dotnet-home",
        "tmp",
        "nuget",
        "smoke",
    ]:
        path = aux / d
        self.rm(path, recursive=True, force=True)
        self.mkdir(path, parents=True)

    # The Alpine stage0 SDK is only used to bootstrap the build. It links
    # against GCC's libstdc++/libgcc, so provide those privately.
    self.do(
        "cp",
        "-a",
        "bootstrap-pkg/usr/lib/dotnet/bootstrap/10.0.113/.",
        str(auxc / "bootstrap") + "/",
    )

    # The stage0 bootstrap and artifacts packages both contribute NuGet
    # packages to the previously-source-built package directory.
    self.do(
        "sh",
        "-c",
        f"cp -a artifacts-pkg/usr/lib/dotnet/artifacts/10.0.113/. {auxc}/artifacts/ && "
        f"cp -a bootstrap-pkg/usr/lib/dotnet/artifacts/10.0.113/. {auxc}/artifacts/",
    )

    self.do(
        "sh",
        "-c",
        f"cp -a libstdcxx-pkg/usr/lib/libstdc++.so.6* {auxc}/gcc-libs/ && "
        f"cp -a libgcc-pkg/usr/lib/libgcc_s.so.1 {auxc}/gcc-libs/",
    )

    # The source archives are only needed to populate the directories above.
    # The merged artifacts directory uses hardlinks, so these can be dropped.
    for d in [
        "bootstrap-pkg",
        "artifacts-pkg",
        "libstdcxx-pkg",
        "libgcc-pkg",
    ]:
        self.rm(d, recursive=True, force=True)

    # The matching previously-source-built artifacts carry MSBuild 18.0.11;
    # the VMR's default is 18.0.2, which is not in that archive.
    props = self.cwd / "eng/Versions.props"
    text = props.read_text()
    text = text.replace(
        "<MicrosoftBuildVersion>18.0.2</MicrosoftBuildVersion>",
        "<MicrosoftBuildVersion>18.0.11</MicrosoftBuildVersion>",
    )
    props.write_text(text)

    # The VMR tarball omits the prebuilt-usage baseline. Accept the set
    # produced by this source build (MSBuild 18.0.11 and the 10.0.12
    # packages from the matching source-built artifacts).
    (self.cwd / "eng/tools/prebuilt-baseline.xml").write_text(
        (self.files_path / "prebuilt-baseline.xml").read_text()
    )

    # The build scripts use GNU grep and GNU tar options that the base
    # BSD userland versions lack.
    self.ln_s("/usr/bin/ggrep", aux / "tools" / "grep")
    self.ln_s("/usr/gnubin/find", aux / "tools" / "find")
    self.ln_s("/usr/gnubin/xargs", aux / "tools" / "xargs")
    self.ln_s("/usr/bin/gtar", aux / "tools" / "tar")
    self.ln_s("/usr/bin/gmake", aux / "tools" / "make")
    self.ln_s("/usr/bin/samu", aux / "tools" / "ninja")

    manifest = f"""\
{{
  "release": "10.0.13",
  "channel": "10.0",
  "tag": "v{pkgver}",
  "sdkVersion": "{_sdkver}",
  "runtimeVersion": "10.0.13",
  "aspNetCoreVersion": "10.0.13",
  "sourceRepository": "https://github.com/dotnet/dotnet",
  "sourceVersion": "4099f83977f4d29604a9aeb971fb0a7bc1d5f699",
  "officialBuildId": "20261004.4"
}}
"""
    with open(aux / "release.json", "w") as f:
        f.write(manifest)


def _build_env(self):
    auxc = self.chroot_statedir / "aux"

    cflags = self.get_cflags(hardening=[], shell=True)
    cxxflags = self.get_cxxflags(hardening=[], shell=True)
    cflags += ' -D_GNU_SOURCE -DLIBC_SO=\\"libc.musl-x86_64.so.1\\"'
    cxxflags += ' -D_GNU_SOURCE -DLIBC_SO=\\"libc.musl-x86_64.so.1\\"'

    env = {
        "CC": "/usr/bin/clang",
        "CXX": "/usr/bin/clang++",
        "CLR_CC": "/usr/bin/clang",
        "CLR_CXX": "/usr/bin/clang++",
        "CFLAGS": cflags,
        "CXXFLAGS": cxxflags,
        "LDFLAGS": self.get_ldflags(hardening=[], shell=True),
        "DOTNET_ROOT": str(auxc / "bootstrap"),
        "DOTNET_INSTALL_DIR": str(auxc / "bootstrap"),
        "DOTNET_CLI_HOME": str(auxc / "dotnet-home"),
        "DOTNET_CLI_TELEMETRY_OPTOUT": "1",
        "DOTNET_SKIP_FIRST_TIME_EXPERIENCE": "1",
        "DOTNET_NOLOGO": "1",
        "DOTNET_SYSTEM_NET_DISABLEIPV6": "1",
        "DOTNET_LTTng": "0",
        "DOTNET_BUNDLE_EXTRACT_BASE_DIR": str(auxc / "tmp"),
        "HOME": str(auxc / "dotnet-home"),
        "NUGET_PACKAGES": str(auxc / "nuget"),
        "TMPDIR": str(auxc / "tmp"),
        "LD_LIBRARY_PATH": str(auxc / "gcc-libs"),
        "PATH": ":".join(
            [
                str(auxc / "tools"),
                str(auxc / "bootstrap"),
                "/usr/bin",
                "/bin",
            ]
        ),
        "LANG": "C.UTF-8",
        "CI": "",
    }

    args = [
        f"/m:{self.make_jobs}",
        "/v:minimal",
        "/p:LogVerbosity=minimal",
        "/p:MinimalConsoleLogOutput=true",
        "/p:CleanWhileBuilding=true",
        "/p:OfficialBuilder=Alpine",
        "/p:ContinueOnPrebuiltBaselineError=true",
        "/p:SkipErrorOnPrebuilts=true",
        "/p:TargetRid=linux-musl-x64",
        "/p:DefaultSubsets=clr+libs+tools+host+packs+tasks",
        "/p:CMakeArgs=-DHeimdalGssApi=OFF",
        "/p:FeatureXplatEventSource=false",
        "/p:UseSystemLibs=+brotli+zlib+libunwind-lttng",
    ]

    return auxc, env, args


def prepare(self):
    auxc, env, args = _build_env(self)

    # Populate the prebuilt/reference package caches used by the
    # source-build-assets step.
    self.do(
        "./prep-source-build.sh",
        "--with-sdk",
        str(auxc / "bootstrap"),
        "--bootstrap-rid",
        "linux-musl-x64",
        env=env,
        allow_network=True,
    )

    # The source build restores NuGet packages, so it has to run in a phase
    # with network access; the build phase itself is offline.
    self.do(
        "./build.sh",
        "--with-sdk",
        str(auxc / "bootstrap"),
        "--with-packages",
        str(auxc / "artifacts"),
        "--release-manifest",
        str(auxc / "release.json"),
        "--source-only",
        "--",
        *args,
        env=env,
        allow_network=True,
    )


def build(self):
    auxc = self.chroot_statedir / "aux"

    # Smoke test the produced SDK and verify it does not pull in GCC runtime
    # libraries.
    archive = _sdk_archive(self)
    self.do("tar", "xzf", archive, "-C", str(auxc / "smoke"), "--no-same-owner")
    self.do(
        str(auxc / "smoke" / "dotnet"),
        "--info",
        env={
            "DOTNET_ROOT": str(auxc / "smoke"),
            "DOTNET_CLI_HOME": str(auxc / "dotnet-home"),
            "HOME": str(auxc / "dotnet-home"),
            "TMPDIR": str(auxc / "tmp"),
            "PATH": "/usr/bin:/bin",
            "LANG": "C.UTF-8",
        },
    )
    _check_no_gcc(self, str(auxc / "smoke"))


def install(self):
    archive = _sdk_archive(self)

    self.install_dir("usr/lib/dotnet")
    self.do(
        "tar",
        "xzf",
        archive,
        "-C",
        str(self.chroot_destdir / "usr/lib/dotnet"),
        "--no-same-owner",
    )

    root = self.destdir / "usr/lib/dotnet"

    for path in root.glob(
        "shared/Microsoft.NETCore.App/*/libcoreclrtraceptprovider.so"
    ):
        path.unlink()

    _fix_modes(self, root)

    _check_no_gcc(self, str(self.chroot_destdir / "usr/lib/dotnet"))

    self.install_dir("usr/bin")
    self.install_link("usr/bin/dotnet", "../lib/dotnet/dotnet")
    if (root / "dnx").is_file():
        self.install_link("usr/bin/dnx", "../lib/dotnet/dnx")

    self.install_file(self.files_path / "dotnet.sh", "etc/profile.d")
    self.install_file(self.files_path / "install_location", "etc/dotnet")
    self.install_file(self.files_path / "install_location_x64", "etc/dotnet")

    self.install_completion(
        "src/sdk/scripts/register-completions.bash", "bash", "dotnet"
    )
    self.install_completion(
        "src/sdk/scripts/register-completions.zsh", "zsh", "dotnet"
    )

    self.install_license("LICENSE.TXT")
