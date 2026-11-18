pkgname = "opencode"
pkgver = "2.2.5"
pkgrel = 2
archs = ["x86_64"]
_nodepty_ver = "1.2.0-beta.12"
_ffirs_commit = "d93e1748d68f5f688e9d57cb8efa8e4007ac29f4"
hostmakedepends = [
    "cargo-bootstrap",
    "clang",
    "git",
    "gmake",
    "libcxx-devel",
    "libgcc-chimera",
    "nodejs",
    "python",
    "rust",
]
makedepends = ["linux-headers"]
depends = [
    "ca-certificates",
    "curl",
    "libcxx",
    "libcxxabi",
    "libgcc-chimera",
    "libunwind",
    "openbsd",
]
pkgdesc = "Open source AI coding agent"
license = "MIT"
url = "https://github.com/anomalyco/opencode"
source = [
    f"{url}/archive/refs/tags/v{pkgver}.tar.gz",
    f"https://registry.npmjs.org/node-pty/-/node-pty-{_nodepty_ver}.tgz",
    f"https://github.com/zhangyuang/node-ffi-rs/archive/{_ffirs_commit}.tar.gz",
]
source_paths = [".", "node-pty", "ffi-rs"]
sha256 = [
    "04621edf6c47c2c7a36982ef39914d482c16977708fbd7b779f49f928bdc4fba",
    "45a012e37699bb70c9050cbf2e06e71b0b842de4cda58e938e3de973f6d5a36a",
    "5015ad7c332562ca98ae1a99d816a3428f44e9a26982ed038c6efd5405936e2e",
]
# the single-executable binary cannot be stripped, and tests need a browser
options = ["!check", "!cross", "!debug", "!lto", "!strip"]

# Bun-only build driver files, ported to Node APIs
_node_files = {
    "script-index.ts": "packages/script/src/index.ts",
    "app-assets.ts": "packages/cli/script/app-assets.ts",
    "verify-artifact.ts": "packages/cli/script/verify-artifact.ts",
    "models-snapshot.ts": "packages/core/script/models-snapshot.ts",
    "runtime-modules.ts": "packages/plugin/src/runtime-modules.ts",
    "target.ts": "packages/cli/src/node/target.ts",
    "node-assets.ts": "packages/cli/script/node-assets.ts",
    "build-node.ts": "packages/cli/script/build-node.ts",
}


def prepare(self):
    self.cp(self.files_path / "flatten-bun.mjs", "flatten-bun.mjs")
    self.cp(self.files_path / "apply-patches.mjs", "apply-patches.mjs")

    # OpenCode uses Bun's catalog and workspace protocols; flatten them for npm
    self.do(
        "node",
        "flatten-bun.mjs",
        ".",
        env={"OPENCODE_TARGET_LIBC": "musl"},
    )

    # Rollup 4.68.6 (2026-11-18) regresses on ordinary modules with
    # "Code is nested too deeply"; pin the previous release.
    self.do(
        "node",
        "-e",
        'const fs=require("fs");const p="package.json";'
        'const d=JSON.parse(fs.readFileSync(p,"utf8"));'
        'd.overrides=Object.assign({},d.overrides,{rollup:"4.68.5"});'
        'fs.writeFileSync(p,JSON.stringify(d,null,2)+"\\n");',
    )

    self.do(
        "npm",
        "install",
        "--ignore-scripts",
        "--no-audit",
        "--no-fund",
        "--legacy-peer-deps",
        "--allow-git=all",
        "--allow-file=all",
        "--force",
        env={
            "HOME": "/tmp/npm-home",
            "npm_config_cache": "/cbuild_cache/npm",
        },
        allow_network=True,
    )

    self.do("node", "apply-patches.mjs", ".")

    # Node's V8 rejects the \p{Surrogate} Unicode property that vite uses;
    # the equivalent surrogate range works.
    for p in self.cwd.rglob("vite/dist/node/chunks/*.js"):
        text = p.read_text()
        if r"\p{Surrogate}" in text:
            p.write_text(text.replace(r"\p{Surrogate}", r"[\uD800-\uDFFF]"))

    for src, dest in _node_files.items():
        self.cp(self.files_path / "node" / src, dest)

    # the Node build's internal binary name is opencode2-node; install as opencode
    # upstream's Node prelude hardcodes OPENTUI_LIBC="glibc", so OpenTUI looks
    # for the glibc native asset even though we embed the musl one; select musl
    # for it and for the watcher/fff fallbacks as well
    cfg = self.cwd / "packages/cli/vite.node.config.ts"
    cfg.write_text(
        cfg.read_text()
        .replace(
            'OPENCODE_CLI_NAME: JSON.stringify("opencode2-node")',
            'OPENCODE_CLI_NAME: JSON.stringify("opencode")',
        )
        .replace(
            'process.env.OPENTUI_LIBC = "glibc"',
            'process.env.OPENTUI_LIBC = "musl"',
        )
        .replace(
            'OPENCODE_LIBC: input.target.platform === "linux" ? JSON.stringify("glibc") : "undefined"',
            'OPENCODE_LIBC: input.target.platform === "linux" ? JSON.stringify("musl") : "undefined"',
        )
        .replace(
            'FFF_LIBC: input.target.platform === "linux" ? JSON.stringify("gnu") : "undefined"',
            'FFF_LIBC: input.target.platform === "linux" ? JSON.stringify("musl") : "undefined"',
        )
    )

    # build a musl node-pty addon in place of the glibc prebuild npm fetched
    self.do(
        "npm",
        "install",
        "--ignore-scripts",
        "--no-audit",
        "--no-fund",
        "--omit=dev",
        "node-addon-api@7",
        wrksrc="node-pty",
        env={"HOME": "/tmp/npm-home", "npm_config_cache": "/cbuild_cache/npm"},
        allow_network=True,
    )
    # node-gyp calls plain `make`; the Oasis userland ships sbase make as
    # /usr/bin/make, so give it GNU make through a PATH shim
    self.mkdir("make-bin", parents=True)
    (self.cwd / "make-bin/make").symlink_to("/usr/bin/gmake")
    makebin = str(self.chroot_cwd / "make-bin")

    # libffi's libtool probes GCC's -print-multi-os-directory; clang does not
    # implement it, so answer like GCC through a wrapper.
    self.mkdir("tool-bin", parents=True)
    for name in ("clang", "clang++"):
        p = self.cwd / "tool-bin" / name
        p.write_text(
            "#!/bin/sh\n"
            'for a in "$@"; do\n'
            '    [ "$a" = "-print-multi-os-directory" ] && { echo .; exit 0; }\n'
            "done\n"
            f'exec /usr/bin/{name} "$@"\n'
        )
        p.chmod(0o755)
    toolbin = str(self.chroot_cwd / "tool-bin")

    self.do(
        "node",
        "/usr/lib/node_modules/npm/node_modules/node-gyp/bin/node-gyp.js",
        "rebuild",
        wrksrc="node-pty",
        env={
            "CC": "clang",
            "CXX": "clang++",
            "CXXFLAGS": "-stdlib=libc++ -O2",
            "LDFLAGS": "-stdlib=libc++",
            "npm_config_nodedir": "/usr",
            "PATH": makebin + ":/usr/bin:/bin",
        },
    )
    self.cp(
        "node-pty/build/Release/pty.node",
        "node_modules/@lydell/node-pty-linux-x64/prebuilds/linux-x64/pty.node",
    )

    # the watcher's musl prebuild is linked against libstdc++; rebuild it
    self.do(
        "node",
        "/usr/lib/node_modules/npm/node_modules/node-gyp/bin/node-gyp.js",
        "rebuild",
        wrksrc="node_modules/@parcel/watcher",
        env={
            "CC": "clang",
            "CXX": "clang++",
            "CXXFLAGS": "-stdlib=libc++ -O2",
            "LDFLAGS": "-stdlib=libc++",
            "npm_config_nodedir": "/usr",
            "PATH": makebin + ":/usr/bin:/bin",
        },
    )
    self.cp(
        "node_modules/@parcel/watcher/build/Release/watcher.node",
        "node_modules/@parcel/watcher-linux-x64-musl/watcher.node",
    )

    # ffi-rs ships a prebuilt linked against libgcc_s; build it with libunwind
    self.do(
        "cargo",
        "build",
        "--release",
        "--locked",
        wrksrc="ffi-rs",
        env={
            "CC": toolbin + "/clang",
            "CXX": toolbin + "/clang++",
            "CARGO_HOME": "/cbuild_cache/cargo",
            "PATH": makebin + ":" + toolbin + ":/usr/bin:/bin",
        },
        allow_network=True,
    )
    self.cp(
        "ffi-rs/target/release/libffi_rs.so",
        "node_modules/@yuuang/ffi-rs-linux-x64-musl/ffi-rs.linux-x64-musl.node",
    )


def build(self):
    self.mkdir("home", parents=True)
    home = str(self.chroot_cwd / "home")

    self.do(
        "node",
        str(self.chroot_cwd / "node_modules/.bin/tsx"),
        "script/build-node.ts",
        "--skip-install",
        wrksrc="packages/cli",
        env={
            "HOME": home,
            "NODE_BIN": "/usr/bin/node",
            "OPENCODE_TARGET": "linux-x64",
            "OPENCODE_VERSION": pkgver,
            "OPENCODE_CHANNEL": "latest",
            "OPENCODE_LIBC": "musl",
        },
    )

    # generate completions as the invoking user; the SEA asset cache rejects
    # paths owned by another uid, which fakeroot in the install phase triggers
    out = "packages/cli/dist/node/cli-node-linux-x64/bin/opencode"
    self.do("cp", out, "opencode")
    self.do("chmod", "755", "opencode")
    for shell in ["bash", "fish", "zsh"]:
        self.do(
            "sh",
            "-c",
            f"./opencode --completions {shell} > opencode.{shell}",
            env={"HOME": home},
        )


def install(self):
    out = "packages/cli/dist/node/cli-node-linux-x64/bin/opencode"
    self.install_bin(out, name="opencode")

    self.install_file(
        "opencode.bash",
        "usr/share/bash-completion/completions",
        name="opencode",
    )
    self.install_file(
        "opencode.fish",
        "usr/share/fish/vendor_completions.d",
        name="opencode.fish",
    )
    self.install_file(
        "opencode.zsh", "usr/share/zsh/site-functions", name="_opencode"
    )

    self.install_license("LICENSE")
