# Oasis minimal source-bootstrap cports

A trimmed [`cports`](https://github.com/chimera-linux/cports) tree that
contains exactly the source templates needed to run:

```
./cbuild source-bootstrap
```

That is the point of this tree: a Linux system with the bootstrap host tools
can build the cbuild bootstrap environment from source, then start adding
packages.

## The package list

`main/` contains **66 source templates**: the stage 0 + stage 1 dependency
closure of `main/base-cbuild`, as computed by cbuild. Stage 1 and stage 2 have
the same dependency set.

This is deliberately not the 175-template closure you get from
`print-build-graph` on an unmodified tree. That graph includes the stage-3
`ccache` dependency that upstream `base-cbuild` adds at `stage > 2`. ccache's
runtime closure pulls in `elfutils -> libmicrohttpd -> gnutls -> unbound ->
protobuf -> boost`, plus `util-linux`, `trousers`, and friends. None of that
is needed to bootstrap.

This tree applies one local patch (`patches/0001-base-cbuild-drop-ccache.patch`)
that removes that optional stage-3 ccache dependency. With it, stages 0–3 all
need the same 66 templates, and `boost`, `util-linux`, `doxygen`, `gtest`,
`protobuf`, `abseil-cpp`, Sphinx, and DocBook tooling are absent.

## What is in here

| Path | Purpose |
|---|---|
| `cbuild`, `src/` | cbuild itself (imported from upstream cports) |
| `main/` | 66 source-bootstrap templates + subpackage symlinks |
| `user/` | empty category for packages you add |
| `bootstrap-packages.txt` | pinned manifest of the 66 templates |
| `patches/` | local template patches (ccache removal) |
| `etc/build_profiles/` | architecture profiles |
| `etc/apk/` | Chimera repository definitions and signing keys |
| `etc/config.ini` | minimal local config (`categories = main user`) |
| `tools/import-bootstrap-closure.sh` | re-import engine, templates, patches |
| `tools/verify-bootstrap-closure.sh` | verify manifest ↔ template graph |
| `tools/compute-bootstrap-closure.py` | recompute the stage 0/1 closure |
| `tools/bootstrap.sh` | optional binary bldroot shortcut |

## Provenance

Engine and templates were imported from a local checkout of
`chimera-linux/cports` (fork `jmalcolm137/cports`) at commit:

```
81f424235f6122f0c93a26797f0e63229e9d0736
halcyon-extra/samurai: new package
2026-11-12
```

## Host requirements

`source-bootstrap` stage 0 runs on the host, so the host must already have the
initial toolchain:

- Python 3.12+, `apk-tools` 3.x, `bubblewrap`, `git`, `openssl`
- `clang` with `lld`, `libc++`, `compiler-rt`, LLVM `libunwind`
- GNU `make` as `make`, GNU `m4` as `m4`
- `cmake`, `meson`, `ninja`, `pkg-config`
- `byacc` (or `bison` with a `yacc` symlink), `flex`, `perl`
- `strip`
- Linux kernel headers for userland

A musl-based host is required. On Chimera, this is the
`base-cbuild-bootstrap` metapackage. On Oasis, provide these via pkgsrc or
equivalent.

## First-time setup

```
./cbuild keygen
```

This writes `etc/keys/oasis-local.rsa{,.pub}`, matching `etc/config.ini`.

## Build the bootstrap from source

```
./cbuild source-bootstrap
```

This builds stages 0–3 using only the 66 templates in `main/`. It is long
(LLVM, clang, musl, Python, etc.) and writes `bldroot-stage*`,
`packages-stage*`, and finally `bldroot/`.

You can stop after a specific stage:

```
./cbuild source-bootstrap 0
```

## Add packages

Put a template in `user/<name>/` and build it:

```
./cbuild pkg user/<name>
```

Included templates can also be built directly, e.g. `./cbuild pkg main/lz4`.

If a package needs a dependency that is not in `main/`, either add that
template to `user/` or (for the binary path) rely on the remote repository.

## Optional: binary build environment

If you do not want to wait for a source bootstrap, `tools/bootstrap.sh`
assembles `bldroot/` from binary Chimera `base-cbuild` packages. That is a
shortcut for building packages immediately; it is not part of the 66-template
source bootstrap.

## Verify the tree

```
tools/verify-bootstrap-closure.sh
```

It checks the manifest is sorted and unique, every template exists, `main/`
has no templates outside the manifest, subpackage symlinks resolve, every
template parses and lints, and the local build graph matches the 66-entry
manifest exactly. The graph check also proves the ccache/boost/util-linux
branch has not come back.

## Refresh from upstream

```
tools/import-bootstrap-closure.sh /path/to/cports
```

The import script clears `main/`, copies exactly the manifest, applies
`patches/*.patch`, and recreates subpackage symlinks. It only writes inside
this directory. To recompute the closure from an upstream checkout:

```
tools/compute-bootstrap-closure.py /path/to/cports 0 1
```
