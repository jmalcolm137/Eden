# Oasis-composed cbuild environment

A minimal local [`cports`](https://github.com/chimera-linux/cports) tree that
assembles an Oasis-flavoured cbuild environment.

**Policy:** Oasis first, pkgsrc second, Chimera only when neither provides what
is needed. Chimera is currently used for the compiler toolchain, musl recipe,
GNU make naming, bsdtar/libarchive, fakeroot, apk-tools, and the OpenSSL
libraries apk-tools links against.

## Local templates (25)

Oasis / local:

```
acl          awk           base-cbuild     base-files     bearssl
bzip2        ca-certificates diffutils     gmake          grep
libedit      libffi8       linux-personality lz4          musl
ncurses      oksh          patch           pigz           sbase
sed          ubase         xz              zlib-ng-compat zstd
```

The current bottom layer of the bldroot is built from these templates.

## Current bldroot

`bldroot-oasis` has 54 packages. The following are now source-built from the
local templates:

```
acl awk base-cbuild base-files bearssl bzip2 ca-certificates diffutils
gmake grep libedit libffi8 lz4 musl musl-devel musl-ldso musl-progs
ncurses-libs oksh patch pigz sbase sed ubase xz zlib-ng-compat zstd
zstd-progs
```

Still binary from Chimera:

```
apk-tools apk-tools-static-bin clang clang-cpp-libs clang-libs
clang-rt-devel fakeroot-core fortify-headers libarchive-progs
libatomic-chimera libatomic-chimera-devel libcxx libcxxabi libcxxabi-devel
libcxx-devel libunwind libunwind-devel lld llvm llvm-binutils llvm-libs
llvm-linker-tools llvm-runtime openssl3-libs
```

No `chimerautils`, no `debianutils`, no OpenSSL CLI.

## Deliberate exceptions

| Item | Choice | Reason |
|---|---|---|
| libc | Chimera musl recipe | requested; local template is Chimera's musl |
| make | Oasis `make`, Chimera `gmake` | cbuild uses gmake explicitly; `/usr/bin/make` stays sbase |
| tar | Chimera bsdtar | sbase tar does not auto-decompress `.gz`/`.xz`/`.zst` |
| strings/getconf | Chimera llvm-binutils/musl | same packages provide required strip/objcopy and musl ABI |
| grep/sed/diff/patch | pkgsrc-version GNU tools | sbase grep/sed are rejected by autoconf; GNU diff/patch required |
| OpenSSL | Chimera `openssl3-libs` | apk-tools links `libcrypto.so.3` and `libssl.so.3` |
| ncurses | Chimera `ncurses-libs` for now | netbsd-curses is Oasis's preference, but Chimera libedit/LLVM link `libncursesw.so.6`; swapping needs those rebuilt against netbsd-curses |

## Layout

| Path | Purpose |
|---|---|
| `cbuild`, `src/` | cbuild engine plus local patches |
| `main/` | 25 local templates and subpackage symlinks |
| `user/` | add your own package templates here |
| `patches/` | engine patches: gmake invocation, apk TLS cert path |
| `etc/build_profiles/` | architecture profiles |
| `etc/apk/` | Chimera repo config, Chimera keys, local public key |
| `etc/config.ini` | local config (`categories = main user`) |
| `tools/bootstrap-oasis.sh` | build environment in a temporary Chimera root |
| `tools/sync-engine.sh` | refresh engine/profiles/repo config from cports |
| `tools/verify-bootstrap-closure.sh` | verify templates, composition, patches |
| `bootstrap-packages.txt` | manifest of local templates |

## Build

```
./cbuild keygen          # once
tools/bootstrap-oasis.sh
```

The script creates a temporary Chimera root (`bldroot-chimera`), builds all
local templates into `.bootstrap-repo` in dependency order (with
`base-cbuild` last), then creates `bldroot-oasis`.

Important: build environment packages in `bldroot-chimera`, not in
`bldroot-oasis`. `sbase`'s install script needs `awk`; rebuilding it inside
the Oasis root after its own tools were removed produces an empty package.

Then build packages with:

```
./cbuild -r .bootstrap-repo -b bldroot-oasis pkg user/<name>
```

## Engine patches

- `patches/0001-cbuild-use-gmake.patch`: cbuild uses `gmake` for GNU make,
  while Oasis `make` remains `/usr/bin/make`.
- `patches/0002-cbuild-ssl-cert-env.patch`: set `SSL_CERT_FILE` for apk inside
  the bldroot, using the static Oasis CA bundle.

Refresh the engine with:

```
tools/sync-engine.sh /path/to/cports
```

The script reapplies all patches and never touches `main/` or `user/`.

## Verify

```
tools/verify-bootstrap-closure.sh
```

Checks manifest ↔ template directories, subpackage symlinks, parsing, linting,
the Oasis/Chimera split in `base-cbuild`, the gmake rename, and the engine's
`make_cmd`.

## Validated

- `tools/bootstrap-oasis.sh` completes from a clean state.
- `bldroot-oasis` builds and contains the 54 packages above.
- All bottom-layer packages are source-built and selected over the Chimera
  binaries.
- `./cbuild -r .bootstrap-repo -b bldroot-oasis pkg main/ubase` succeeds.
- `make`, `gmake`, `awk`, `grep`, `sed`, `diff`, `cmp`, `patch`, `cut`, `tar`,
  and `gzip` all resolve inside the bldroot.

## Next

Move up from the bottom layer: `apk-tools`, `fakeroot`, `libarchive`,
`libatomic-chimera`, `fortify-headers`, then the LLVM/clang stack. OpenSSL and
the ncurses ABI remain the main deliberate binary dependencies.
