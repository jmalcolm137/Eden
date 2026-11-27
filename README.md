# The Linux Eden Project

Eden is a Linux distribution heavily inspired by OASIS Linux. It could be considered a port. Compared to OASIS Linux, it is significantly more "batteries included".

The goal is a Linux distribution that is fully capable but also simple enough to fully inspect and understand. While not a fully "suckless" distribution, Eden does prefer minimalism where possible.

The ISO released on November 20, 2026 boots into a live environment almost identical to OASIS Linux on that date.

The live environment boots to a Wayland desktop running in 100 MB of RAM.

The 400 MB ISO includes a tiling Wayland compositor, fully working C compiler, Python, media player, BitTorrent client, web browser, web server, OpenSSH client/server, and a comprehensive suite of utilities.
But OASIS offers all this as well.

Relative to OASIS, what extra batteries are included?

## Complete build system

Eden leverages the excellent [`cbuild`](https://github.com/chimera-linux/cports) system from Chimera Linux.

"suckless" fans will be horrified that this requires Python to compile a C program. But OASIS relies on LUA for the same purpose (LUA not required on Eden) and Eden continues to embrace minimalism. For example, cbuild replaces meson/ninja with muon/samurai and OpenSSL has been fully supplanted by BearSSL (or LibreSSL where required).

cbuild brings Eden complete dependency management for the entire distribution. All software is built in a container, isolating the build from contamination and ensuring complete reproducibility.

The entire distribution, including the bootable ISO, can be built from source with a single script.

cbuild makes it very easy to port software to Eden.

## A complete toolchain

OASIS Linux includes the cproc C compiler but it is broken as OASIS does not include a pre-processor. Eden ships mcpp so cproc is fully working out-of-the-box. But even on OASIS, cproc is not meant to be the system compiler. OASIS Linux does not ship or specify one.

Eden uses Clang/LLVM as the system compiler and it is included as part of the distribution. All software is built and tested with this version. This includes libc++, compiler-rt, libunwind, lld, and llvm-binutils.

Like Alpine, Adelie, OASIS, and Chimera Linux, Eden uses musl as its C library. Like Chimera Linux, it uses mimalloc as the memory allocator in musl. Unlike Chimera Linux, Eden uses the mimalloc 3.x release.

## A fully specified kernel

Eden includes cbuild instructions for a Linux kernel based on the kernel from CachyOS. A complementary suite of tools is also provided including kmod, mkinitramfs, ckms (from Chimera Linux), and the limine boot manager.

## A package manager with online repositories

Eden uses apk, the Alpine Package Keeper package management system from Alpine Linux.

cbuild does not directly build and install software. Instead, it builds binary packages which are made available to apk to install, upgrade, remove, etc.

It is possible to build all packages from source and to install them locally but apk defaults to retrieving packages from the cloud.

Are the "suckless" utilities too limiting? `apk add gnu-compat` installs a fully GNU compatible userland.

Do you need more advanced development capabilities?

`apk add clang`

`apk add rust`

`apk add zig`

`apk add dotnet`

The Velox tiling compositor is not your thing? `apk add xfce4-desktop` and you have an advanced Wayland desktop in moments.

Compiling all the above from source could take days. Much of this software is difficult to port (especially to musl/libc++).

NetBSD pkgsrc, while excellent, can be hit-or-miss on a system like OASIS. Of course, it is still there if you want it.

All Eden packages can be built from source using cbuild if you prefer.

## cbuild repositories

| Repo | Purpose |
|---|---|
| `core/` | Everything needed to source-bootstrap the bldroot |
| `oasis/` | Packages required to build a full OASIS system |
| `pkgsrc/` | Packages ported from pkgsrc that do not belong in core/oasis |
| `extra/` | Additional packages not present in the other repos |

The categories are layered with `.parent` symlinks:

```
core <- oasis <- pkgsrc <- extra
```

Registry config uses `categories = core oasis pkgsrc extra`. The stage-0 bldroot is installed
from the published Eden mirror at `https://repos.eden-linux.org`, and every
package is then rebuilt from the templates in this tree. The other binary
inputs are the official Rust stage0 tarballs used by
`rust-bootstrap`/`cargo-bootstrap`.

### core templates (61)

```
acl apk-tools argp-standalone attr awk base-cbuild base-files base-kernel bc
bearssl bubblewrap byacc bzip2 ca-certificates ckms cmake curl elfutils
fakeroot flex fortify-headers git gmake gnu-m4 gperf gsed kmod libatomic-
chimera libcap libedit libffi8 libressl libtls-bearssl linux-headers linux-
kernel linux-personality llvm llvm-bootstrap lz4 mandoc muon musl musl-bsd-
headers musl-fts musl-obstack nasm netbsd-curses oksh openbsd perl pigz
pkgconf python samurai sbase ubase ugetopt unzip xz zlib zstd
```

### oasis templates (192)

```
acme-client acpid adobe-source-fonts alsa-lib alsa-lib-devel atinout autoconf
automake b3sum b3sum-devel binutils blind cacert catgirl cmark cmark-devel
cmark-devel-static cproc dav1d dav1d-devel dmenu dnssec-rr dosfstools
e2fsprogs e2fsprogs-devel efibootmgr efivar efivar-devel expat f2fs-tools
farbfeld ffmpeg ffmpeg-devel file file-devel fontconfig fontconfig-devel
freetype freetype-devel fribidi fribidi-devel fspec-sync fuse fuse-devel
gettext gettext-devel hostapd hotplugd hyx ii iproute2 jbig2dec jbig2dec-devel
kbd less libass libass-devel libbluray libbluray-devel libcbor libcbor-devel
libdrm libdrm-devel libevdev libevdev-devel libevent libevent-devel libevent-
devel-static libexpat libexpat-devel libexpat-progs libffi libfido2
libfido2-devel libgpiod libgpiod-devel libinput libinput-devel libjpeg-turbo
libjpeg-turbo-devel libliftoff libliftoff-devel libnl libnl-devel libpciaccess
libpciaccess-devel libplacebo libplacebo-devel libpng libpng-devel libtermkey
libtirpc libtirpc-devel libtool libtool-devel libtool-libs libutp libutp-devel
libxkbcommon libxkbcommon-devel libxml2 libxml2-devel libxml2-progs lpeg lua
luaposix make man-pages-posix mblaze mcpp mcpp-doc mgba mpv msmtp mtdev mtdev-
devel mupdf mupdf-devel ncompress netsurf nginx nsd openntpd openssh opus
opus-devel opus-devel-static pax pciutils pciutils-devel pcre pcre-devel pcre-
devel-static pdpmake perp pixman pixman-devel pounce pwgen qbe quark rc sdhcp
sfeed sinit skeleton sndio snes9x squashfs-tools-ng sshfs st strace swc swc-
devel syslinux syslogd terminus-font texi2mdoc the_silver_searcher tinyalsa
tinyalsa-devel tinyalsa-devel-static tinyemu transmission tz u-boot u-config
udev udev-devel unbound usbids utf8proc util-linux util-linux-devel util-
linux-libs-static velox vis wayland wayland-devel wayland-progs wayland-
protocols wireguard-tools wl9 wld wld-devel wpa_supplicant x509cert x509cert-
devel x509cert-devel-static xkeyboard-config yt-dlp zfs
```

### pkgsrc templates (215)

```
aardvark-dns adwaita-icon-theme adwaita-icon-theme-legacy atk atk-devel bash
bison brotli brotli-devel brotli-progs cairo cairo-devel cargo-bootstrap
cbindgen conmon crun crun-devel dbus dbus-devel dbus-libs enchant2
enchant2-devel enchant2-progs firefox font-util font-util-devel fuse3
fuse3-devel gdk-pixbuf gdk-pixbuf-devel glib glib-devel glib-networking gmp
gmp-cxx gmp-devel gnutls gnutls-devel go go-bootstrap go-md2man grep gst-
plugins-base gst-plugins-base-devel gstreamer gstreamer-devel gstreamer-progs
gtar gtk+3 gtk+3-devel gtk-layer-shell gtk-layer-shell-devel harfbuzz
harfbuzz-devel hicolor-icon-theme hicolor-icon-theme-devel htop hwdata hwdata-
devel hwdata-net hwdata-pci hwdata-pnp hwdata-usb icu icu-devel icu-progs isl
iso-codes json-c json-c-devel json-glib json-glib-devel just krb5 krb5-devel
libburn libburn-devel libburn-progs libcanberra libcanberra-devel libcurl
libcurl-devel libdisplay-info libdisplay-info-devel libepoxy libepoxy-devel
libexif libexif-devel libfontenc libfontenc-devel libglvnd libglvnd-devel
libgtop libgtop-devel libgudev libgudev-devel libisofs libisofs-devel libjpeg-
turbo libjpeg-turbo-devel libjpeg-turbo-progs libndp libndp-devel libnotify
libnotify-devel libogg libogg-devel libpsl libpsl-devel libpulse libpulse-
devel libseat libseat-devel libseat-progs libseccomp libseccomp-devel
libseccomp-progs libsndfile libsndfile-devel libssh2 libssh2-devel libtasn1
libtasn1-devel libtasn1-progs libtirpc libtirpc-devel libuuid libuuid-devel
libvorbis libvorbis-devel libx11 libx11-devel libxau libxau-devel libxcb
libxcb-devel libxcvt libxcvt-devel libxcvt-progs libxdmcp libxdmcp-devel
libxfont2 libxfont2-devel libxkbfile libxkbfile-devel libxshmfence
libxshmfence-devel libxslt libxslt-devel libxslt-progs libyaml libyaml-devel
limine linux-firmware linux-firmware-amdgpu linux-firmware-broadcom linux-
firmware-intel linux-firmware-nvidia linux-firmware-radeon meson-real
mkinitcpio mpcomplex mpfr mtools netavark nettle nettle-devel nettle-progs
networkmanager networkmanager-devel networkmanager-libs nghttp2 nghttp2-devel
nodejs oniguruma oniguruma-devel openssl openssl-progs pango pango-devel
patchelf pcre2 pcre2-devel pipewire pipewire-devel podman polkit polkit-devel
polkit-libs pop-launcher protoc-bootstrap pulseaudio pulseaudio-progs ripgrep
rust rust-bootstrap shared-mime-info sqlite sqlite-devel taglib taglib-devel
upower upower-devel upower-libs uutils-coreutils uutils-findutils wireplumber
xcbproto xorg-util-macros xorgproto xserver-xorg-protocol xtrans xwayland
xwayland-devel zlib-shared
```

### extra templates (146)

```
antigravity-cli catfish cosmic-app-library cosmic-applets cosmic-bg cosmic-
comp cosmic-desktop cosmic-edit cosmic-files cosmic-icons cosmic-idle cosmic-
launcher cosmic-monitor cosmic-notifications cosmic-osd cosmic-panel cosmic-
player cosmic-randr cosmic-screenshot cosmic-session cosmic-settings cosmic-
settings-daemon cosmic-sound-theme cosmic-store cosmic-term cosmic-viewer
cosmic-wallpapers cosmic-workspaces dbus-glib dbus-glib-devel dotnet exo exo-
devel fast_float garcon garcon-devel gigolo gleam gnu-compat gobject-
introspection gobject-introspection-devel gobject-introspection-libs goose
goose-extension goose-samples gspell gspell-devel gtksourceview4
gtksourceview4-devel libnma libnma-devel libsecret libsecret-devel libsoup3
libsoup3-devel libucontext libxfce4ui libxfce4ui-devel libxfce4util
libxfce4util-devel libxfce4windowing libxfce4windowing-devel mesa mesa-devel
mesa-gbm-devel mesa-gbm-libs mesa-libgallium mousepad network-manager-applet
opencode parole python-dbus python-gobject python-mako python-markdown python-
markupsafe python-packaging python-pexpect python-ptyprocess python-pyyaml
python-setuptools ristretto smithay thunar thunar-archive-plugin thunar-devel
thunar-media-tags-plugin thunar-vcs-plugin thunar-volman tumbler tumbler-devel
vte-gtk3 vte-gtk3-devel xdg-desktop-portal xdg-desktop-portal-cosmic xfburn
xfce4-appfinder xfce4-battery-plugin xfce4-calculator-plugin xfce4-clipman-
plugin xfce4-cpufreq-plugin xfce4-cpugraph-plugin xfce4-desktop xfce4-dev-
tools xfce4-dict xfce4-diskperf-plugin xfce4-docklike-plugin xfce4-eyes-plugin
xfce4-fsguard-plugin xfce4-generic-slider xfce4-genmon-plugin xfce4-goodies
xfce4-mailwatch-plugin xfce4-mount-plugin xfce4-netload-plugin xfce4-notes-
plugin xfce4-notifyd xfce4-panel xfce4-panel-devel xfce4-panel-profiles
xfce4-places-plugin xfce4-power-manager xfce4-pulseaudio-plugin
xfce4-screenshooter xfce4-sensors-plugin xfce4-session xfce4-session-devel
xfce4-settings xfce4-smartbookmark-plugin xfce4-stopwatch-plugin
xfce4-systemload-plugin xfce4-taskmanager xfce4-terminal xfce4-time-out-plugin
xfce4-timer-plugin xfce4-verve-plugin xfce4-wavelan-plugin xfce4-weather-
plugin xfce4-whiskermenu-plugin xfconf xfconf-devel xfconfd-lite xfdesktop
xfwl4 xfwm4-themes zig
```

## Current bldroot

`bldroot-oasis` is built from the Oasis-composed `base-cbuild`. The following
are now source-built from the local templates:

```
acl apk-tools apk-tools-static-bin awk base-cbuild base-files bearssl
bzip2 ca-certificates clang clang-cpp-libs clang-libs clang-rt-devel
diffutils fakeroot-core fortify-headers gmake libarchive-progs
libatomic-chimera libatomic-chimera-devel libcxx libcxxabi libcxxabi-devel
libcxx-devel libedit libffi8 libunwind libunwind-devel lld llvm
llvm-binutils llvm-libs llvm-linker-tools llvm-runtime lz4 muon musl
musl-devel musl-ldso musl-progs netbsd-curses oksh patch pigz pkgconf
samurai sbase ubase xz zlib zstd zstd-progs
```

The stage-0 root itself is installed from the published Eden repositories,
so even the initial toolchain is ours.

`apk-tools` is source-built with **BearSSL for both crypto and libfetch
TLS**. Python uses the core LibreSSL package for `ssl` and `hashlib`, and
`cbuild keygen` uses LibreSSL's `openssl` CLI; no OpenSSL package is used.

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

The Oasis Wayland utilities are static-pie linked: `libswc.a` embeds libinput,
libxkbcommon, wayland-server, wld and their static dependencies, and
`swc`, `velox`, `dmenu`, `st`, `wl9`, `swc-launch` and the `velox`
`status_bar` helper have musl linked into the executable with no dynamic
interpreter. `sbase`, `ubase`, `apk-tools`, `netsurf`, and the LLVM/clang
toolchain (`clang`, `clang++`, `lld`, `llvm-config`, `opt`, and the other
tools) are built the same way. The OASIS command-line tools are also
static-pie: `awk`, `byacc`, `bubblewrap`, `bzip2`, `curl`, `file`, `flex`,
`fribidi`, `git`, `libpng`'s `pngfix` tools, `muon`, `oksh`, `pciutils`,
`pigz`, `samurai`, `wayland-scanner`, and `zstd`.

`apk-tools` installs the static-pie `apk` as `/usr/bin/apk`; the separate
`apk-tools-static-bin` package still provides `apk.static`. The LLVM build
uses `llvm-bootstrap`'s static C++ runtime archives, links every executable
with `-static-pie`, and keeps the shared `libLLVM.so` and `libclang-cpp.so`
only for packages that consume them.

## Deliberate exceptions

| Item | Choice | Reason |
|---|---|---|
| libc | Chimera musl recipe | requested; local template is Chimera's musl |
| make | Oasis `make`, Chimera `gmake` | cbuild uses gmake explicitly; `/usr/bin/make` stays sbase |
| tar | Chimera bsdtar | sbase tar does not auto-decompress `.gz`/`.xz`/`.zst` |
| strings/getconf | Chimera llvm-binutils/musl | same packages provide required strip/objcopy and musl ABI |
| grep/sed/diff/patch | sbase sed, GNU gsed/diff/patch, pkgsrc GNU grep | `/usr/bin/sed` stays sbase; GNU sed is packaged as `gsed` (autoconf's `AC_PROG_SED` picks it up); `gnu-compat` links it at `/usr/gnubin/sed`. GNU diff/patch are required. GNU grep is kept for reliability; sbase grep passes the test in isolation |
| OpenSSL | **removed** | apk-tools uses BearSSL; Python and cbuild keygen use LibreSSL from core |
| ncurses | **removed** | libedit is rebuilt against static Oasis netbsd-curses, so it no longer links `libncursesw.so.6`; the bldroot carries no ncurses |

## Layout

| Path | Purpose |
|---|---|
| `cbuild`, `src/` | cbuild engine plus local patches |
| `core/` | core templates and subpackage symlinks |
| `oasis/` | Oasis system packages and their Oasis-sourced dependencies |
| `pkgsrc/`, `extra/` | ported/local package repositories |
| `patches/` | engine patches: gmake, apk TLS cert path, core category, muon/samurai |
| `etc/build_profiles/` | architecture profiles |
| `etc/apk/` | Eden repo config and local public key |
| `etc/config.ini` | local config (`categories = core oasis pkgsrc extra`, Eden mirror) |
| `/usr/gnubin` | GNU tool names (`make`, `sed`, `m4`, and the uutils coreutils/findutils applets) installed by `gnu-compat`; `/etc/profile` puts it after `/usr/local/bin` and before `/usr/bin` |
| `tools/bootstrap-oasis.sh` | build environment in a temporary stage-0 root |
| `tools/sync-engine.sh` | refresh engine/profiles/repo config from cports |
| `tools/verify-bootstrap-closure.sh` | verify templates, composition, patches |
| `tools/publish-repo.sh` | publish built repositories to Cloudflare R2 |
| `docs/r2-repos.md` | R2 bucket, custom domain, cache and client setup |
| `bootstrap-packages.txt` | core template manifest |
| `oasis-packages.txt` | oasis template manifest |
| `pkgsrc-packages.txt`, `extra-packages.txt` | other repo manifests |

## Build

```
./cbuild keygen          # once
tools/bootstrap-oasis.sh
```

The script creates a temporary stage-0 root (`bldroot-stage0`) from the
published Eden repositories, builds the core templates into `.bootstrap-repo`
in dependency order (with `base-cbuild` last), then creates `bldroot-oasis`.

Important: build environment packages in `bldroot-stage0`, not in
`bldroot-oasis`. `sbase`'s install script needs `awk`; rebuilding it inside
the Oasis root after its own tools were removed produces an empty package.

Then build packages with:

```
./cbuild -r .bootstrap-repo -b bldroot-oasis pkg extra/<name>
```

## Publishing

Built repositories can be published to Cloudflare R2 at
**https://repos.eden-linux.org**:

```
tools/publish-repo.sh --dry-run
tools/publish-repo.sh --prune --verify
```

The script uploads packages before indexes, keeps the signing key at
`/keys/oasis-local.rsa.pub`, and sets immutable caching on packages and
`no-cache` on indexes. See `docs/r2-repos.md` for the bucket, custom domain,
cache rules, credentials, and client repository configuration.

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
- `patches/0006-cbuild-remote-repo-deps.patch`: include the profile's remote
  repository categories when collecting dependency repositories.
- `patches/0007-cbuild-eden-mirror.patch`: default the apk mirror to
  `https://repos.eden-linux.org` instead of Chimera.

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

- `tools/bootstrap-oasis.sh` completes from a clean tree using only
  `https://repos.eden-linux.org`; no Chimera repository is consulted.
- `bldroot-oasis` is installed from the locally rebuilt stage-0 repository
  (60 packages) and `./cbuild -r .bootstrap-repo -b bldroot-oasis pkg
  core/ubase` succeeds in it.
- All bottom-layer packages are source-built and selected over the stage-0
  binaries.
- `./cbuild -r .bootstrap-repo -b bldroot-oasis pkg core/ubase` succeeds.
- `make`, `gmake`, `awk`, `grep`, `sed`, `diff`, `cmp`, `patch`, `cut`, `tar`,
  and `gzip` all resolve inside the bldroot.

## libtls-bearssl

`oasis/libtls-bearssl` builds the Oasis libtls implementation on BearSSL. Its
shared library needs only `libbearssl.so` and `libc.so`; it does not need
OpenSSL or libbsd. It is built in the `oasis` repository and is not part of the
core bldroot.

## cproc and qbe

`oasis/qbe` and `oasis/cproc` package the compiler pair used by Oasis. The
sources are pinned to the commits in the Oasis `pkg/cproc/src` and
`pkg/qbe/src` submodules, and `oasis/cproc/files/config.h` is Oasis's target
configuration. The preprocessor is set to `clang-cpp` because Chimera's clang
package does not install `/usr/bin/cpp`. Assembly and linking use clang's
integrated assembler and `ld.lld` instead of GNU binutils, so `cproc` depends
on `clang`, `lld`, `musl-devel`, and `qbe`.

## vis

`oasis/vis` packages the `vis` editor at the commit pinned by the Oasis
`pkg/vis/src` submodule. It is built against Oasis's Lua 5.5, lpeg, and
libtermkey, all linked statically, with `netbsd-curses` providing the terminal
interface. The two Oasis patches are applied: the wide-string workaround for
`vis-digraph` and Lua 5.5 support.

## netsurf

`oasis/netsurf` packages the Oasis NetSurf fork with its tiny Wayland
frontend. The build bundles Oasis's pinned versions of libcss, libdom,
libhubbub, libnsbmp, libnsgif, libnsutils, libparserutils, libsvgtiny, and
libwapcaplet, and applies the Oasis patches to them. The system libraries it
needs are also Oasis ports: `curl`, `expat`, `freetype`, `libffi`,
`libjpeg-turbo`, `libpng`, `libxkbcommon`, `pixman`, `utf8proc`, `wayland`,
and `zlib`. The `netsurf` binary is static-pie linked: the bundled
libraries and all of the listed system libraries are linked from their static
archives. At runtime it also needs the Adobe Source fonts (packaged as
`adobe-source-fonts`), xkeyboard-config data, and a Wayland compositor.

## perp and sinit

`oasis/perp` packages the Oasis process supervision suite with Oasis's five
fixup patches applied. All commands and runtools are installed in `/usr/bin`,
matching the Oasis package layout.

`oasis/sinit` packages the Oasis init at the commit pinned by the
`pkg/sinit/src` submodule. It uses Oasis's `config.h` and `shutdown.c`
overrides, installs `sinit` plus the `/usr/bin/init` link, and puts the shutdown
helper in `/usr/lib/sinit/shutdown`.

## velox

`oasis/velox` packages the Oasis Wayland compositor at the commit pinned by
the Oasis `pkg/velox/src` submodule. It builds the compositor itself and
installs the sample configuration; its `swc`, `wld`, `libinput`, `libdrm`,
`libevdev`, `mtdev`, `fontconfig`, and `util-linux` dependencies still need to
be ported from Oasis before it can be built in this tree.

## smithay

`extra/smithay` packages the Smithay Wayland compositor library at the commit
`xfwl4` 4.21.1 pins for its `smithay` and `smithay-drm-extras` git dependencies
(`0a29aecf9e07a2227712ab470b0ab0ee56752272`). Since Smithay is a Rust library
with no C ABI, the package installs the crate source tree under
`/usr/share/cargo/registry/smithay-0.7.0` instead of a shared object. A
dependent package points its path dependencies at that tree, which also avoids
fetching the git dependency during its own offline build:

```python
smithay = { path = "/usr/share/cargo/registry/smithay-0.7.0" }
smithay-drm-extras = {
    path = "/usr/share/cargo/registry/smithay-0.7.0/smithay-drm-extras",
}
```

The build uses the `desktop` and `wayland_frontend` features, which need no
system graphics libraries; the test run also enables the renderer test harness
for the doctests. Compositor-specific backends are enabled by the dependent
package.

## xfwl4

`extra/xfwl4` packages the 4.21.1 release of the Xfce Wayland compositor. The
release tarball already carries the `xfce-wayland-protocols` submodule, so it
is a single source. Upstream's meson build only drives cargo, so the template
builds with cbuild's cargo style and installs the binary, the session desktop
entry, the default settings file and the gettext catalogs itself. It is built
Wayland-only (`udev,egl,gettext-system,xwayland`, no winit/X11; the
`xwayland` feature is only needed by upstream's unconditionally compiled
shell code and `start_xwayland()` is patched out) and replaces
the pinned Smithay git dependency with the source tree from `extra/smithay`,
so no git checkout is needed during the build.

It builds against the Wayland-only toolkit in `pkgsrc/` and `extra/`: shared
`wayland` 1.26.0, `libinput` 1.31.3, `pixman` 0.46.4, `libxkbcommon` 1.13.2,
`libdrm` 2.4.134, plus the GTK3 stack (`glib`, `gtk+3`, `pango`, `cairo`,
`gdk-pixbuf`), the locally built `mesa` (Wayland/GBM with the llvmpipe and
softpipe drivers), `libseat`, `udev` and `libdisplay-info`.
The matching `xfconf`/`libxfce4ui` 4.21 libraries provide
`libxfce4kbd-private-3`. Window decorations are provided by
`extra/xfwm4-themes`; the X11 `xfwm4` compositor is not installed.

## Xfce 4

`extra/` also carries the Xfce 4.21 desktop built for Wayland only. The
umbrella is `xfce4-desktop`; `xfce4-goodies` adds the remaining applications
and panel plugins. X11 is disabled in every component that has a switch
(`-Dx11=disabled`, `-Dwayland=enabled`) and the X11-only pieces are not
packaged: `xfwm4` (only its themes, as `xfwm4-themes`), `xfce4-xkb-plugin`,
`xfce4-windowck-plugin`, and `xfce4-screensaver` (it needs PAM and X11
locking). `xfce4-mount-plugin` is not in the umbrellas because the musl base lacks the
BSD `fstab.h` API. `xfce4-notes-plugin` uses `meson-real` for its Vala rules
but is still blocked by missing GObject-introspection GIR data in the local
`glib` build. Python applications use local 3.15 builds of `python-gobject`,
`python-dbus` and `python-pexpect`; `parole` uses the local `dbus-glib`.

The Wayland-only toolkit closure is local as well. `pixman`, `wayland`,
`wayland-protocols`, `libxkbcommon`, `libinput`, `libdrm`, `freetype`,
`fontconfig`, `fribidi` and `libpng` are the Oasis packages, upgraded in
place, so there are no duplicate X11 and Wayland variants of the same
library. `glib`, `atk`, `harfbuzz`, `cairo`, `pango`, `gdk-pixbuf`, `gtk+3`,
`gtk-layer-shell`, `libdisplay-info`, `pcre2`, `libglvnd`, `libepoxy` and
`meson-real` live in `pkgsrc/`; `gtk+3` is configured with
`-Dx11_backend=false -Dwayland_backend=true`. `mesa`, `vte`,
`gtksourceview`, `gspell`, `libsoup3`, gstreamer and the Xfce stack live in
`extra/`. Every one of these is built from a local template; no `main`
package is used. See [`extra/XFCE4.md`](extra/XFCE4.md) for the exact
versions, the excluded components and the optional features that are still
disabled.

## Next

`tools/bootstrap-oasis.sh` builds the local core set (including the
LLVM/clang stack) into `.bootstrap-repo` and creates the minimal
`bldroot-oasis`. Build the desktop on top of it in dependency order:

```sh
./cbuild -b bldroot-oasis pkg extra/xfce4-desktop
./cbuild -b bldroot-oasis pkg extra/xfce4-goodies
```

