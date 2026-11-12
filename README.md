# Oasis-composed cbuild environment

A minimal local [`cports`](https://github.com/chimera-linux/cports) tree that
builds an Oasis-flavoured cbuild environment:

- **Chimera** supplies the toolchain and low-level build packages:
  `clang`/`llvm`/`lld`, `gmake`, `musl`, `apk-tools`, `fakeroot-core`,
  `libarchive-progs` (bsdtar), and their runtime dependencies.
- **Oasis** supplies the userland: `sbase`, `ubase`, `oksh`, `pigz`,
  `base-files`, and a small personality shim.
- **pkgsrc** is expected to supply host-side tools for running cbuild itself
  (`python`, `git`, `openssl`, `bubblewrap`, etc.).

The result is a working `bldroot-oasis` without `chimerautils`.

## Local templates

Only eight source templates are maintained here:

| Template | Role |
|---|---|
| `base-cbuild` | local meta package: Chimera toolchain + Oasis userland |
| `base-files` | minimal filesystem and `/etc/passwd`/`group` for the bldroot |
| `gmake` | GNU make, exposed only as `/usr/bin/gmake` |
| `linux-personality` | `linux64`/`linux32` shims used by cbuild's sandbox |
| `oksh` | Oasis `/bin/sh` |
| `pigz` | `gzip`/`gunzip`/`zcat` provider |
| `sbase` | Oasis core utilities, including `/usr/bin/make` |
| `ubase` | Oasis base utilities |

Everything else is installed as a binary package from the Chimera repository.

## Conflict policy

Oasis tools are preferred where they work. The exceptions are deliberate:

| Conflict | Winner | Why |
|---|---|---|
| libc / getconf | **Chimera musl** | requested explicitly; musl-progs provides getconf |
| make | **both** | Oasis `make` stays `/usr/bin/make`; Chimera `gmake` is `/usr/bin/gmake`, and cbuild is patched to invoke `gmake` |
| tar | **Chimera bsdtar** | sbase tar does not auto-decompress `.gz`/`.xz`/`.zst` |
| strings | **Chimera llvm-binutils** | the same package must provide `strip`, `objcopy`, `readelf`, etc. |
| gzip | **Oasis pigz** | provides gzip-compatible names |
| debianutils | **transitive** | pulled by Chimera `ca-certificates`/`apk-tools`; sbase/ubase cover the commands we use |

## Layout

| Path | Purpose |
|---|---|
| `cbuild`, `src/` | cbuild engine, with local patches |
| `main/` | the eight local templates and their subpackage symlinks |
| `user/` | add your own package templates here |
| `patches/` | local engine patches (gmake, apk TLS cert path) |
| `etc/build_profiles/` | architecture profiles |
| `etc/apk/` | Chimera repo definitions, Chimera keys, local public key |
| `etc/config.ini` | local config (`categories = main user`) |
| `tools/bootstrap-oasis.sh` | build the whole environment |
| `tools/sync-engine.sh` | refresh engine/profiles/repo config from a cports checkout |
| `tools/verify-bootstrap-closure.sh` | verify templates, composition, engine patches |
| `bootstrap-packages.txt` | manifest of the local templates |

## Build the environment

```
./cbuild keygen          # once
tools/bootstrap-oasis.sh
```

The script:

1. creates `bldroot-chimera` from binary Chimera `base-cbuild`, with its
   complete Chimerautils userland (needed to build gmake/autoconf),
2. builds the local templates into `.bootstrap-repo`, starting with `gmake`,
3. assembles `bldroot-oasis` from the local `base-cbuild`.

Then build packages with:

```
./cbuild -b bldroot-oasis pkg user/<name>
```

or use the included templates:

```
./cbuild -b bldroot-oasis pkg main/ubase
```

## Engine patches

- `patches/0001-cbuild-use-gmake.patch`: default `make_cmd` is `gmake`, and
  cbuild's generated packaging Makefiles, strip helper, and u-boot style use
  `gmake`. This lets Oasis `make` remain `/usr/bin/make`.
- `patches/0002-cbuild-ssl-cert-env.patch`: set `SSL_CERT_FILE` for apk
  invocations inside the bldroot. The minimal `base-files` does not ship
  hashed cert symlinks, but does provide the CA bundle.

Refresh the engine with:

```
tools/sync-engine.sh /path/to/cports
```

The script reapplies every patch and never touches `main/` or `user/`.

## Verify

```
tools/verify-bootstrap-closure.sh
```

Checks the manifest, template directories, subpackage symlinks, parsing,
linting, the Oasis/Chimera split in `base-cbuild`, the gmake rename, and the
engine's `make_cmd`.

## Validated

- `tools/bootstrap-oasis.sh` completes from a clean state.
- `bldroot-oasis` has 50 packages, no `chimerautils`.
- `make` is sbase; `gmake` is GNU make; `tar` handles `.xz` and `.zst`.
- `./cbuild -b bldroot-oasis pkg main/ubase` builds and packages successfully.

## Known gap

The Oasis userland is intentionally small. Some autoconf-based packages
reject sbase `grep`, and sbase does not provide `awk` or `patch`. The
temporary Chimera root covers this while building the environment, but
building arbitrary autoconf packages in `bldroot-oasis` may require adding a
small compatibility layer (GNU grep, one-true-awk, patch) or selectively
using Chimera packages for those tools.

`./cbuild source-bootstrap` is not used here: it would rebuild the whole
Chimera bootstrap chain, including `chimerautils`, which defeats the purpose
of this fork.
