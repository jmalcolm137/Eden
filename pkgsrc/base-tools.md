# The pkgsrc base: tools a package relies on to build

pkgsrc has no single "base" package set. It has:

1. a small **bootstrap kit** it installs into the prefix, and
2. a **per-OS table of tools** it borrows from the host when present.

A package's actual requirement is the union of the two, filtered by its
`USE_TOOLS` and `BUILDLINK` dependencies. This note records what those layers
contain, for use when porting pkgsrc packages into this tree.

## 1. What must exist before pkgsrc can bootstrap

The `bootstrap/` script needs a working POSIX-ish host:

- **Toolchain:** `cc`/`cpp`, `ld`, `as`, `ar`, `ranlib`, `nm`, `strip` (plus
  `objcopy` for some packages)
- **Shell + make:** `/bin/sh` and a native `make` (only to build `bmake`)
- **POSIX userland:** `awk`, `sed`, `grep`, `tr`, `cut`, `sort`, `uniq`,
  `find`, `xargs`, `tar`, `gzip`, `cp`, `mv`, `rm`, `ln`, `mkdir`, `install`,
  `chmod`, `chown`, `cmp`, `diff`, `patch`, `expr`, `basename`, `dirname`,
  `env`, `pwd`, `test`/`[`, `date`, `touch`, `wc`, `head`, `tail`, `tee`,
  `sleep`, `mktemp`, `hostname`, `id`, `nice`, `tsort`, ...

Anything missing here can be built by bootstrap, but the compiler and shell are
hard prerequisites.

## 2. The bootstrap kit

These are the packages pkgsrc treats as its own base -- the literal "pkgsrc
base". They are built by `bootstrap/bootstrap` and installed into the prefix.

| Package | Provides |
|---|---|
| `pkgtools/bootstrap-mk-files` | the `bsd.*.mk` framework itself |
| `devel/bmake` | pkgsrc's `make`; the mk framework requires bmake semantics |
| `pkgtools/libnbcompat` | BSD libc compatibility library |
| `pkgtools/pkg_install` | `pkg_add`, `pkg_delete`, `pkg_info`, `pkg_admin`, `pkg_create` (bundles static libarchive) |

Built conditionally when the host lacks a usable equivalent:

| Package | Condition |
|---|---|
| `sysutils/install-sh` or `sysutils/bsdinstall` | no BSD-compatible `install` |
| `shells/mksh` / `shells/pdksh` | no suitable `sh`/`ksh` |
| `lang/nawk` | no usable `awk` |
| `textproc/nbsed` | host `sed` is deficient |
| `archivers/pax` | no `pax` |
| `pkgtools/bootstrap-extras` | missing `strip`/`mkdir`/`xargs` behaviour |
| `pkgtools/cwrappers` | compiler wrappers in use |
| `pkgtools/mktools` | wrapper/mktool framework in use |

Notably `pkgtools/digest` is **not** bootstrap-kit -- it is pulled in as an
ordinary tool dependency (`TOOLS_DEPENDS.digest`) unless the platform supplies
one.

## 3. The tool inventory the mk framework knows about

`mk/tools/defaults.mk` defines the universe; `mk/tools/tools.<OPSYS>.mk` maps
each to a host path via `TOOLS_PLATFORM.<tool>?=`. Missing ones are promoted to
package dependencies by `<tool>.mk`.

| Group | Tools |
|---|---|
| Shell/core | `sh`, `[`, `test`, `echo`, `printf`, `true`, `false`, `expr`, `env`, `pwd`, `sleep`, `nice`, `id`, `hostname`, `date`, `touch`, `mktemp`, `shlock`, `tsort` |
| Filesystem | `cat`, `cp`, `mv`, `rm`, `rmdir`, `mkdir`, `ln`, `ls`, `chmod`, `chgrp`, `chown`, `install`, `find`, `basename`, `dirname`, `readlink`, `realpath`, `mtree`, `file` |
| Text | `awk`/`gawk`, `sed`/`gsed`, `grep`/`egrep`/`fgrep`, `cut`, `tr`, `sort`, `uniq`, `head`, `tail`, `wc`, `diff`, `diff3`, `sdiff`, `cmp`, `patch` |
| Archives/compression | `tar`/`gtar`, `pax`, `gzip`, `gunzip`, `zcat`/`gzcat`, `bzip2`, `bzcat`, `xz`, `xzcat`, `lzcat`, `zstd`, `unzip`, `lha`, `unrar`, `unzoo`, `7za`, `rpm2pkg` |
| Build/dev | `make`/`gmake`, `m4`/`gm4`, `yacc`/`byacc`/`bison-yacc`, `lex`, `cmake`, `cpack`, `perl`, `tclsh`, `wish`, `gem`, `git`, `imake`, `xmkmf`, `pkg-config` |
| Docs | `nroff`, `groff`, `tbl`, `soelim`/`gsoelim`, `makeinfo`, `install-info`, `mandoc`, `pod2man` |
| Misc | `openssl`, `mail`, `digest` |
| Shells | `bash`, `csh`, `ksh` |

A package only wires up the ones it names in `USE_TOOLS` (plus
implicit/`BUILDLINK`-implied ones); the rest are just resolution rules.

## 4. On NetBSD specifically

NetBSD base already provides the framework equivalents: `/usr/bin/make` is
bmake, `pkg_install` is `/usr/sbin/pkg_*`, and `pax`, `mtree`, `tar`, `awk`,
`sed`, etc. are in base.

`mk/tools/tools.NetBSD.mk` lists the concrete host paths, including `awk`,
`byacc`, `bsdtar`, `bzip2`, `cat`, `chgrp`, `chmod`, `chown`, `cmp`, `cp`,
`csh`, `cut`, `date`, `diff`, `diff3`, `dirname`, `env`, `expr`, `file`,
`find`, `flex`, `ftp`, `gettext`, `grep`/`egrep`/`fgrep`, `groff`, `gzip`/
`gunzip`/`gzcat`, `head`, `hostname`, `id`, `install`, `ksh`, `lex`, `ln`,
`ls`, `m4`, `mail`, `mandoc`, `mkdir`, `mktemp`, `mtree`, `mv`, `nice`,
`nroff`, `openssl`, `patch`, `pax`, `printf`, `pwd`, `readelf`, `readlink`,
`rm`, `rmdir`, `sdiff`, `sed`, `sh`, `shlock`, `sleep`, `sort`, `strip`,
`tail`, `tar`, `tbl`, `tee`, `test`, `touch`, `tr`, `true`, `tsort`, `uniq`,
`wc`, `xargs`, `xz`, `yacc`. All are `?=` so `mk.conf` can override them.
`digest` is still built from `pkgtools/digest`.

## 5. Bearing on this tree

cbuild is not pkgsrc, so the `bmake` + `pkg_install` + `libnbcompat` kit does
not apply -- `core/` is the functional equivalent. When porting a `pkgsrc/`
package, translate its `USE_TOOLS` into build-env dependencies rather than
expecting pkgsrc's tool framework.

`bldroot-oasis` already covers nearly all of the POSIX/toolchain layer:

```
sbase/ubase, oksh, awk, sed, grep, diffutils, patch, gmake,
bsdtar/bsdcpio, pigz/gzip, bzip2, xz, zstd, lz4, pkgconf,
perl, python, cmake, muon/samu, clang/lld/llvm-binutils
```

The gaps a port is most likely to hit are `m4` (template exists at `core/m4`
but is not in `base-cbuild`'s `depends`), `unzip`, `groff`/`makeinfo`,
`openssl`, and `git`.

## Sources

- `pkgsrc/bootstrap/bootstrap`
- `pkgsrc/mk/tools/defaults.mk`
- `pkgsrc/mk/tools/tools.<OPSYS>.mk` (e.g. `tools.NetBSD.mk`, `tools.Linux.mk`)
