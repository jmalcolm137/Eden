# Oasis minimal cports

A trimmed [`cports`](https://github.com/chimera-linux/cports) tree containing
only:

- the `cbuild` engine (Python), and
- the **exact dependency closure of `main/base-cbuild`** — the minimum package
  set cbuild considers necessary to build and run its own build environment —
  plus an empty `user/` category for local packages.

Nothing else from Chimera's 2,000+ package tree is included.

## What is in here

| Path | Purpose |
|---|---|
| `cbuild`, `src/` | cbuild itself (imported from upstream cports) |
| `main/` | 175 bootstrap templates and their subpackage symlinks |
| `user/` | empty category for packages you add |
| `bootstrap-packages.txt` | pinned manifest of the `main/` closure |
| `etc/build_profiles/` | architecture profiles |
| `etc/apk/` | Chimera repository definitions and signing keys |
| `etc/config.ini` | minimal local config (`categories = main user`) |
| `tools/import-bootstrap-closure.sh` | refresh engine + closure from a cports checkout |
| `tools/verify-bootstrap-closure.sh` | check manifest ↔ directories ↔ cbuild graph |

## Provenance

Engine and templates were imported from a local checkout of
`chimera-linux/cports` (fork `jmalcolm137/cports`) at commit:

```
81f424235f6122f0c93a26797f0e63229e9d0736
halcyon-extra/samurai: new package
2026-11-12
```

The closure was computed from that checkout with:

```
./cbuild print-build-graph main/base-cbuild
```

and includes build, runtime, and (because checks are enabled by default)
check dependencies. It is pinned in `bootstrap-packages.txt`; upstream changes
to `base-cbuild`'s dependencies will change the graph, so re-import when you
want to track them.

## Requirements

Same as cbuild:

- Python 3.12+
- `apk-tools` 3.x
- `bubblewrap` (`bwrap`)
- `git`
- `openssl` (key generation)
- Linux 3.8+ with namespaces (`USER_NS`, `PID_NS`, `NET_NS`, `UTS_NS`,
  `IPC_NS`) and cgroups
- a normal user (never root) and not a chroot

For a **source** bootstrap you additionally need GNU make as `make` and GNU
m4 as `m4` (plus clang/lld/libc++/compiler-rt/libunwind, cmake, meson,
pkg-config, ninja, strip, yacc, flex, perl, and Linux kernel headers). See
the upstream `Usage.md`.

## First-time setup

Generate a signing key (once):

```
./cbuild keygen oasis-local
```

This writes `etc/keys/oasis-local.rsa{,.pub}` and is already wired up in
`etc/config.ini`.

## Create the build environment

### Fast path: binary bootstrap

Assembles `bldroot/` from Chimera binary packages, without rebuilding the 175
templates:

```
./cbuild bootstrap
```

Use this for day-to-day package building. The local bootstrap templates are
not used.

### Minimal source bootstrap

Builds only the 175-package closure in `main/`, through cbuild's four stages:

```
./cbuild source-bootstrap
```

This is the "bare minimum from source" path. It is slow (it includes LLVM,
clang, musl, apk-tools, Python, etc.) and is much less frequently tested
upstream than the binary bootstrap. All artifacts stay in this directory:
`bldroot-stage{0,1,2}`, `packages-stage*`, `sources/`, `cbuild_cache/`.

You can stop after a given stage with e.g. `./cbuild source-bootstrap 0`.

## Build packages

Included bootstrap packages can be built directly:

```
./cbuild pkg main/lz4
```

For your own packages, create `user/<name>/template.py` and run:

```
./cbuild pkg user/<name>
```

The resulting signed packages go to `packages/`, and are usable as an apk
repository (add the architecture subdirectory, e.g. `packages/user/x86_64`,
to `/etc/apk/repositories.d/` and install the public key in `/etc/apk/keys`).

## Verify the tree

```
tools/verify-bootstrap-closure.sh
```

It checks that every manifest entry exists, that the manifest is sorted and
unique, and that the graph produced by the local cbuild matches the manifest
exactly. If you add templates to `main/`, the graph check will still pass;
extra templates are intentionally ignored. If you add a package that
`base-cbuild` does not depend on, put it in `user/` instead.

## Refresh from upstream

The tree was imported from a local cports checkout. To pull a newer engine and
the same pinned closure:

```
tools/import-bootstrap-closure.sh /path/to/cports
```

The import script only writes inside this directory. It materializes symlinked
patch directories (`cp -aL`) so the tree stays self-contained, then recreates
subpackage symlinks with `./cbuild relink-subpkgs`.

To update the closure itself, regenerate `bootstrap-packages.txt` from the
upstream checkout using the graph command above, then re-run the import
script and the verifier.

## Validation performed

- `tools/verify-bootstrap-closure.sh` — passes; the locally computed graph
  matches the 175-entry manifest exactly.
- `./cbuild bootstrap` — succeeded; 58 binary packages installed into
  `bldroot/` (561 MiB).
- `./cbuild pkg main/lz4` — succeeded; signed `lz4` and its subpackages were
  written to `packages/main/{,debug/}x86_64/`.

The source bootstrap path has not been executed end-to-end here (it builds
LLVM/clang/musl/Python from source and takes a long time), but its template
closure and dependency graph are verified.

## Notes and limits

- `main/` is not a general-purpose package repository. If you want a package
  outside the closure, import its template (and its dependencies) or use the
  upstream tree.
- `base-cbuild` intentionally contains the full toolchain, so the closure is
  large (LLVM/clang, musl, apk-tools, Python, and their build dependencies).
  That is the minimum cbuild itself declares, not an arbitrary subset.
- Check dependencies are part of the closure because `check` is enabled by
  default. Building a subset with checks disabled does not automatically
  shrink cbuild's dependency graph.
- The `user/` category is scanned even when empty; it is where local work
  belongs.
