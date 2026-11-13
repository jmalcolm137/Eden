# Oasis-composed cbuild environment

A minimal local [`cports`](https://github.com/chimera-linux/cports) tree that
assembles an Oasis-flavoured cbuild environment.

**Policy:** Oasis first, pkgsrc second, Chimera only when neither provides what
is needed.

## Repositories

| Repo | Purpose |
|---|---|
| `core/` | Everything needed to source-bootstrap the bldroot |
| `oasis/` | Packages required to build a full OASIS system |
| `pkgsrc/` | Packages ported from pkgsrc that do not belong in core/oasis |
| `extra/` | Locally created packages not present in the other repos |

The categories are layered with `.parent` symlinks:

```
core <- oasis <- pkgsrc <- extra
```

Registry config uses `categories = core oasis pkgsrc extra main user`; the
`main`/`user` entries only enable the remote Chimera binary repositories.

### core templates (32)

```
acl apk-tools awk base-cbuild base-files bearssl bzip2 ca-certificates
diffutils fakeroot fortify-headers gmake libarchive libatomic-chimera
libedit libffi8 linux-personality lz4 muon musl netbsd-curses oksh
patch pigz pkgconf samurai sbase sed ubase xz zlib-ng-compat zstd
```

### oasis templates (1)

```
libtls-bearssl
```

## Current bldroot

`bldroot-oasis` has 66 packages. The following are now source-built from the
local templates:

```
acl apk-tools apk-tools-static-bin awk base-cbuild base-files bearssl
bzip2 ca-certificates diffutils fakeroot-core fortify-headers gmake
libarchive-progs libatomic-chimera libatomic-chimera-devel libedit
libffi8 lz4 muon musl musl-devel musl-ldso musl-progs netbsd-curses
oksh patch pigz pkgconf samurai sbase sed ubase xz zlib-ng-compat zstd
zstd-progs
```

Still binary from Chimera:

```
clang clang-cpp-libs clang-libs clang-rt-devel
libcxx libcxxabi libcxxabi-devel libcxx-devel
libunwind libunwind-devel lld llvm llvm-binutils
llvm-libs llvm-linker-tools llvm-runtime
```

`apk-tools` is now source-built with **BearSSL for both crypto and libfetch
TLS**; no OpenSSL packages remain in the bldroot.

All Meson-style packages are built with Oasis **muon** and **samurai**; the
engine no longer invokes `meson` or `ninja`. `muon` carries one local patch so
that `library()` with `default_library=both` does not link `link_whole`
dependencies twice.

`libatomic-chimera` is a Chimera runtime shim providing `libatomic.so.1` for
compiler-generated atomic builtins. It is pulled in by clang; cbuild itself
does not call it directly. The `-devel` package is only needed for static
builds.

`netbsd-curses` is built from Oasis and provides static `libcurses`,
`libterminfo`, and the terminfo database. `libedit` is built against it and
embeds the curses code, so neither `libedit` nor `llvm-libs` pulls in
`libncursesw.so.6`.

No `chimerautils`, no `debianutils`, no OpenSSL CLI.

## Deliberate exceptions

| Item | Choice | Reason |
|---|---|---|
| libc | Chimera musl recipe | requested; local template is Chimera's musl |
| make | Oasis `make`, Chimera `gmake` | cbuild uses gmake explicitly; `/usr/bin/make` stays sbase |
| tar | Chimera bsdtar | sbase tar does not auto-decompress `.gz`/`.xz`/`.zst` |
| strings/getconf | Chimera llvm-binutils/musl | same packages provide required strip/objcopy and musl ABI |
| grep/sed/diff/patch | pkgsrc-version GNU tools | GNU sed passes autoconf's non-truncation test (sbase sed truncates); GNU diff/patch are required. GNU grep is kept for reliability; sbase grep passes the test in isolation |
| OpenSSL | **removed** | apk-tools uses BearSSL for crypto and libfetch TLS; no OpenSSL packages remain |
| ncurses | **removed** | libedit is rebuilt against static Oasis netbsd-curses, so it no longer links `libncursesw.so.6`; the bldroot carries no ncurses |

## Layout

| Path | Purpose |
|---|---|
| `cbuild`, `src/` | cbuild engine plus local patches |
| `core/` | core templates and subpackage symlinks |
| `oasis/` | Oasis system packages (`libtls-bearssl`) |
| `pkgsrc/`, `extra/` | ported/local package repositories |
| `patches/` | engine patches: gmake, apk TLS cert path, core category, muon/samurai |
| `etc/build_profiles/` | architecture profiles |
| `etc/apk/` | Chimera repo config, Chimera keys, local public key |
| `etc/config.ini` | local config (`categories = core oasis pkgsrc extra main user`) |
| `tools/bootstrap-oasis.sh` | build environment in a temporary Chimera root |
| `tools/sync-engine.sh` | refresh engine/profiles/repo config from cports |
| `tools/verify-bootstrap-closure.sh` | verify templates, composition, patches |
| `bootstrap-packages.txt` | core template manifest |
| `oasis-packages.txt` | oasis template manifest |
| `pkgsrc-packages.txt`, `extra-packages.txt` | other repo manifests |

## Build

```
./cbuild keygen          # once
tools/bootstrap-oasis.sh
```

The script creates a temporary Chimera root (`bldroot-chimera`), builds the
core templates into `.bootstrap-repo` in dependency order (with `base-cbuild`
last), then creates `bldroot-oasis`.

Important: build environment packages in `bldroot-chimera`, not in
`bldroot-oasis`. `sbase`'s install script needs `awk`; rebuilding it inside
the Oasis root after its own tools were removed produces an empty package.

Then build packages with:

```
./cbuild -r .bootstrap-repo -b bldroot-oasis pkg extra/<name>
```

## Engine patches

- `patches/0001-cbuild-use-gmake.patch`: cbuild uses `gmake` for GNU make,
  while Oasis `make` remains `/usr/bin/make`.
- `patches/0002-cbuild-ssl-cert-env.patch`: set `SSL_CERT_FILE` for apk inside
  the bldroot, using the static Oasis CA bundle.
- `patches/0004-cbuild-core-category.patch`: use `core/` for the hardcoded
  `base-files` and `base-cbuild` paths.
- `patches/0005-cbuild-use-muon-samurai.patch`: invoke `muon` instead of
  `meson`, `samu` instead of `ninja`, and translate meson-only build options
  and dependency names (`meson` -> `muon`, `ninja` -> `samurai`).

Refresh the engine with:

```
tools/sync-engine.sh /path/to/cports
```

The script reapplies all patches and never touches the package repositories.

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
- `./cbuild -r .bootstrap-repo -b bldroot-oasis pkg core/ubase` succeeds.
- `make`, `gmake`, `awk`, `grep`, `sed`, `diff`, `cmp`, `patch`, `cut`, `tar`,
  and `gzip` all resolve inside the bldroot.

## libtls-bearssl

`oasis/libtls-bearssl` builds the Oasis libtls implementation on BearSSL. Its
shared library needs only `libbearssl.so` and `libc.so`; it does not need
OpenSSL or libbsd. It is built in the `oasis` repository and is not part of the
core bldroot.

## Next

The remaining binary set is the LLVM/clang stack. Add an LLVM source template
that links against the local `libedit` built with netbsd-curses and produces
clang, lld, libcxx, libunwind, llvm-binutils, and the rest.

