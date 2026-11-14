import shutil
def _make_crossfile(pkg, build_dir):
    if not pkg.profile.cross:
        return

    cfpath = pkg.cwd / build_dir / "cbuild.cross"

    (pkg.cwd / build_dir).mkdir(parents=True, exist_ok=True)

    # map known profiles to meson arch
    match pkg.profile.arch:
        case "aarch64" | "x86_64" | "riscv64":
            meson_cpu = pkg.profile.arch
        case "ppc64le" | "ppc64":
            meson_cpu = "ppc64"
        case "ppc":
            meson_cpu = "ppc"
        case "armhf" | "armv7":
            meson_cpu = "arm"
        case "loongarch64":
            meson_cpu = "loongarch64"
        case _:
            pkg.error(f"unknown meson architecture: {pkg.profile.arch}")

    with open(cfpath, "w") as outf:
        outf.write(f"""
[binaries]
c = '{pkg.get_tool("CC")}'
cpp = '{pkg.get_tool("CXX")}'
ar = '{pkg.get_tool("AR")}'
nm = '{pkg.get_tool("NM")}'
ld = '{pkg.get_tool("LD")}'
strip = '{pkg.get_tool("STRIP")}'
readelf = '{pkg.get_tool("READELF")}'
objcopy = '{pkg.get_tool("OBJCOPY")}'
pkgconfig = '{pkg.get_tool("PKG_CONFIG")}'
llvm-config = '/usr/bin/llvm-config'
rust = ['rustc', '--target', '{pkg.profile.triplet}', '--sysroot', '{pkg.profile.sysroot / "usr"}']

[properties]
needs_exe_wrapper = true

[built-in options]
c_args = {pkg.get_cflags()}
c_link_args = {pkg.get_ldflags()}

cpp_args = {pkg.get_cxxflags()}
cpp_link_args = {pkg.get_ldflags()}

[host_machine]
system = 'linux'
cpu_family = '{meson_cpu}'
cpu = '{pkg.profile.arch}'
endian = '{pkg.profile.endian}'
""")

    return cfpath


# muon does not implement every meson built-in option; silently drop the
# ones it rejects instead of failing the whole configure step.
_MUON_UNSUPPORTED_OPTS = (
    "pkgconfig.relocatable",
)


def _meson(pkg):
    # Prefer the Oasis tools. Stage 0 builds on the host, so fall back to
    # the host meson when muon has not been installed yet.
    if pkg.stage == 0 and not shutil.which("muon"):
        return "meson"
    return "muon"


def _cross_arg(pkg, path):
    if _meson(pkg) == "muon":
        return "-pcross:" + path
    return "--cross-file=" + path


def _muon_arg(arg):
    # translate meson-style long options into muon's -D form
    if arg.startswith("--") and "=" in arg:
        name, _, val = arg[2:].partition("=")
        if name == "cross-file":
            return "-pcross:" + val
        return f"-D{name.replace('-', '_')}={val}"
    if arg.startswith("-D") and "=" in arg:
        name = arg[2:].split("=", 1)[0]
        if name in _MUON_UNSUPPORTED_OPTS:
            return None
    return arg


def configure(pkg, build_dir, meson_dir=None, extra_args=None, env=None):
    if not meson_dir:
        meson_dir = "."

    # muon misdetects an explicitly-set $AR as ar-solaris, which drops the
    # input/output arguments from its archiver rule. An empty value makes it
    # fall back to the compiler's preferred (posix) archiver.
    env = dict(env or {})
    env.setdefault("AR", "")
    env.setdefault("AR_FOR_BUILD", "")

    # muon's native setup takes a single build directory; its meson
    # compatibility layer is needed when a source subdirectory is requested.
    if _meson(pkg) == "muon":
        if meson_dir and meson_dir != ".":
            setup = ["muon", "meson", "setup"]
            setup_dirs = [meson_dir, build_dir]
        else:
            setup = ["muon", "setup"]
            setup_dirs = [build_dir]
    else:
        setup = ["meson", "setup"]
        setup_dirs = [meson_dir, build_dir] if meson_dir and meson_dir != "." else [build_dir]

    cfp = _make_crossfile(pkg, build_dir)

    cargs = []
    if cfp:
        cargs = [
            _cross_arg(pkg, str(pkg.chroot_cwd / cfp.relative_to(pkg.cwd)))
        ]

    if pkg.has_lto():
        cargs.append("-Db_lto=true")
        # mode, thin is default for us
        if pkg.options["ltofull"]:
            cargs.append("-Db_lto_mode=default")
        else:
            cargs.append("-Db_lto_mode=thin")
    else:
        cargs.append("-Db_lto=false")

    pkg.do(
        *setup,
        "-Dprefix=/usr",
        "-Dlibdir=/usr/lib",
        "-Dlibexecdir=/usr/lib",
        "-Dbindir=/usr/bin",
        "-Dsbindir=/usr/bin",
        "-Dincludedir=/usr/include",
        "-Ddatadir=/usr/share",
        "-Dmandir=/usr/share/man",
        "-Dinfodir=/usr/share/info",
        "-Dsysconfdir=/etc",
        "-Dlocalstatedir=/var",
        "-Dsharedstatedir=/var/lib",
        "-Dbuildtype=plain",
        "-Dauto_features=auto",
        "-Dwrap_mode=nodownload",
        "-Ddefault_library=both",
        "-Dwerror=false",
        "-Db_staticpic=true",
        "-Dpython.bytecompile=0",
        *cargs,
        *(_muon_extra_args(extra_args) if _meson(pkg) == "muon" else (extra_args or [])),
        *setup_dirs,
        env=env,
    )


def _muon_extra_args(extra_args):
    args = []
    for arg in extra_args or []:
        marg = _muon_arg(arg)
        if marg is not None:
            args.append(marg)
    return args


def invoke(pkg, command, build_dir, extra_args=None, env=None, wrapper=None):
    pkg.do(
        *(wrapper or []),
        _meson(pkg),
        command,
        *(extra_args or []),
        wrksrc=build_dir,
        env=env,
    )


def install(pkg, build_dir, extra_args=None, env=None, wrapper=None):
    renv = {"DESTDIR": str(pkg.chroot_destdir)}
    if env:
        renv.update(env)
    args = [*(extra_args or [])]
    if _meson(pkg) == "meson":
        args.insert(0, "--no-rebuild")
    invoke(pkg, "install", build_dir, args, renv, wrapper)


def test(pkg, build_dir, extra_args=None, env=None, wrapper=None):
    if _meson(pkg) == "muon":
        args = ["-R", "-j", str(pkg.make_jobs), *(extra_args or [])]
    else:
        args = [
            "--no-rebuild",
            "--print-errorlogs",
            "--num-processes",
            str(pkg.make_jobs),
            *(extra_args or []),
        ]
    invoke(pkg, "test", build_dir, args, env, wrapper)
