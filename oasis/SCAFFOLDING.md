# Scaffolded Oasis packages

Metadata copied from the Oasis `pkg/` tree for packages that do not yet
have a buildable cbuild template in `core/` or `oasis/`.

Each directory contains the Oasis recipe metadata (`gen.lua`, `ver`,
`config.h`, patches, helper files) and a `SOURCE.txt` describing where
the upstream source comes from.  There is deliberately no `template.py`:
add one only when the package has actually been ported, then list it in
`oasis-packages.txt`.

Scaffolded packages: 110

| Package | Version | Source kind | Source |
| --- | --- | --- | --- |
| `acme-client` | - | source-package | pkg/openbsd |
| `acpid` | 2.0.34-2-g81df3ad695 r0 | git-submodule | https://git.code.sf.net/p/acpid2/code |
| `alsa-lib` | 1.2.11 r1 | git-submodule | https://github.com/alsa-project/alsa-lib.git |
| `atinout` | 0.9.1 r0 | git-submodule | https://git.code.sf.net/p/atinout/code |
| `b3sum` | 1.5.0 r0 | git-submodule | https://git.sr.ht/~mcf/b3sum |
| `bc` | 1.08.2 r0 | tarball | https://ftp.gnu.org/gnu/bc/bc-1.08.2.tar.gz |
| `binutils` | 2.46.0 r1 | tarball | https://ftp.gnu.org/gnu/binutils/binutils-2.46.0.tar.xz |
| `blind` | 1.1 r4 | git-submodule | git://git.suckless.org/blind |
| `bubblewrap` | 0.11.0 r2 | git-submodule | https://github.com/containers/bubblewrap.git |
| `cacert` | 2026-10-20 | tarball | https://curl.se/ca/cacert-2026-10-20.pem |
| `catgirl` | 2.2a | git-submodule | https://git.causal.agency/catgirl |
| `cmark` | 0.31.2 r0 | git-submodule | https://github.com/commonmark/cmark.git |
| `dav1d` | 0.9.2 r0 | git-submodule | https://github.com/videolan/dav1d.git |
| `dmenu` | 4.9 r4 | git-submodule | git://git.suckless.org/dmenu |
| `dnssec-rr` | 0.2 r0 | git-submodule | https://git.sr.ht/~mcf/dnssec-rr |
| `dosfstools` | 4.2 r1 | git-submodule | https://github.com/dosfstools/dosfstools.git |
| `e2fsprogs` | 1.46.4 r2 | git-submodule | https://git.kernel.org/pub/scm/fs/ext2/e2fsprogs.git |
| `efibootmgr` | 18 | git-submodule | https://github.com/rhinstaller/efibootmgr.git |
| `efivar` | 39 | git-submodule | https://github.com/rhinstaller/efivar.git |
| `elftoolchain` | ce6d62aaba r1 | git-submodule |  |
| `f2fs-tools` | 1.14.0 r2 | git-submodule | https://git.kernel.org/pub/scm/linux/kernel/git/jaegeuk/f2fs-tools.git |
| `farbfeld` | 4 r0 | git-submodule | git://git.suckless.org/farbfeld |
| `ffmpeg` | 7.0.2 r1 | git-submodule | https://github.com/ffmpeg/ffmpeg.git |
| `file` | 5.45 r0 | git-submodule | https://github.com/file/file.git |
| `flex` | 2.6.4 r1 | tarball | https://github.com/westes/flex/releases/download/v2.6.4/flex-2.6.4.tar.gz |
| `fontconfig` | 2.13.1 r1 | tarball | https://www.freedesktop.org/software/fontconfig/release/fontconfig-2.13.1.tar.gz |
| `fribidi` | 1.0.11 r0 | git-submodule | https://github.com/fribidi/fribidi.git |
| `fspec-sync` | a79592936c r0 | git-submodule | https://github.com/oasislinux/fspec-sync.git |
| `fuse` | 3.10.5 r2 | git-submodule | https://github.com/libfuse/libfuse.git |
| `hotplugd` | c15eea9bde r0 | git-submodule | https://github.com/oasislinux/hotplugd.git |
| `hyx` | 2026.01.11 r0 | tarball | https://yx7.cc/code/hyx/hyx-2026.01.11.tar.xz |
| `ii` | 1.9 r0 | git-submodule | git://git.suckless.org/ii |
| `iproute2` | 6.8.0 r1 | git-submodule | https://git.kernel.org/pub/scm/linux/kernel/git/shemminger/iproute2.git |
| `jbig2dec` | 0.19 r0 | git-submodule | git://git.ghostscript.com/jbig2dec.git |
| `kbd` | 2.4.0 r0 | tarball | https://www.kernel.org/pub/linux/utils/kbd/kbd-2.4.0.tar.gz |
| `less` | 643 r0 | tarball | http://www.greenwoodsoftware.com/less/less-643.tar.gz |
| `libass` | 0.14.0 r1 | git-submodule | https://github.com/libass/libass.git |
| `libbluray` | 1.3.4 r0 | tarball | https://download.videolan.org/pub/videolan/libbluray/1.3.4/libbluray-1.3.4.tar.bz2 |
| `libcbor` | 0.9.0 r0 | git-submodule | https://github.com/PJK/libcbor.git |
| `libdrm` | 2.4.120 r0 | git-submodule | https://gitlab.freedesktop.org/mesa/drm.git |
| `libevdev` | 1.12.0 r0 | git-submodule | https://gitlab.freedesktop.org/libevdev/libevdev.git |
| `libevent` | 2.1.12 r0 | git-submodule | https://github.com/libevent/libevent.git |
| `libfido2` | 1.9.0 r0 | git-submodule | https://github.com/oasislinux/libfido2.git |
| `libgpiod` | 1.6.3 r1 | git-submodule | https://git.kernel.org/pub/scm/libs/libgpiod/libgpiod.git |
| `libinput` | 1.19.3 r0 | git-submodule | https://github.com/oasislinux/libinput.git |
| `libliftoff` | 0.5.0 0 | git-submodule | https://gitlab.freedesktop.org/emersion/libliftoff.git |
| `libnl` | 3.5.0 r2 | git-submodule | https://github.com/thom311/libnl.git |
| `libpciaccess` | 0.18 r0 | git-submodule | https://gitlab.freedesktop.org/xorg/lib/libpciaccess.git |
| `libplacebo` | 7.349.0 r0 | git-submodule | https://code.videolan.org/videolan/libplacebo.git |
| `libressl` | 4.3.1 r1 | tarball | https://cdn.openbsd.org/pub/OpenBSD/LibreSSL/libressl-4.3.1.tar.gz |
| `libtirpc` | 1.3.7 | git-submodule | git://git.linux-nfs.org/projects/steved/libtirpc.git |
| `libutp` | 996ad97f18 r0 | git-submodule | https://github.com/oasislinux/libutp.git |
| `luaposix` | 36.2.1 r0 | git-submodule | https://github.com/luaposix/luaposix.git |
| `make` | 4.4.1 r1 | tarball | http://ftp.gnu.org/gnu/make/make-4.4.1.tar.gz |
| `man-pages-posix` | 2017a r0 | tarball | https://www.kernel.org/pub/linux/docs/man-pages/man-pages-posix/man-pages-posix-2017-a.tar.gz |
| `mblaze` | 1.4 r0 | git-submodule | https://github.com/leahneukirchen/mblaze.git |
| `mgba` | 0.8.4 r0 | git-submodule | https://github.com/mgba-emu/mgba.git |
| `mpv` | 0.38.0 r1 | git-submodule | https://github.com/mpv-player/mpv.git |
| `msmtp` | 1.8.22 r0 | git-submodule | https://github.com/marlam/msmtp-mirror.git |
| `mtdev` | 1.1.7 r0 | tarball | https://bitmath.se/org/code/mtdev/mtdev-1.1.7.tar.gz |
| `mupdf` | 1.18.0 r1 | git-submodule | https://github.com/oasislinux/mupdf.git |
| `ncompress` | 5.0 r1 | git-submodule | https://github.com/vapier/ncompress.git |
| `nginx` | 1.31.0 | git-submodule | https://github.com/nginx/nginx.git |
| `nsd` | 4.3.6 r0 | tarball | https://www.nlnetlabs.nl/downloads/nsd/nsd-4.3.6.tar.gz |
| `openbsd` | 8.0 | tarball | https://cloudflare.cdn.openbsd.org/pub/OpenBSD/8.0/src.tar.gz |
| `openntpd` | 6.8p1 r0 | tarball | https://cdn.openbsd.org/pub/OpenBSD/OpenNTPD/openntpd-6.8p1.tar.gz |
| `openssh` | 10.6p2 | git-submodule | https://github.com/oasislinux/openssh.git |
| `opus` | 1.5.2 r1 | tarball | https://github.com/xiph/opus/releases/download/v1.5.2/opus-1.5.2.tar.gz |
| `pax` | c2a77c3ea3 | git-submodule | https://git.sr.ht/~mcf/pax |
| `pciutils` | 3.14.0 r0 | git-submodule | https://git.kernel.org/pub/scm/utils/pciutils/pciutils.git |
| `pcre` | 8.45 r0 | tarball | https://sourceforge.net/projects/pcre/files/pcre/8.45/pcre-8.45.tar.gz |
| `pdpmake` | 2.0.4 | git-submodule | https://github.com/rmyorston/pdpmake.git |
| `pounce` | 3.0 r0 | git-submodule | https://git.causal.agency/pounce |
| `pwgen` | 2.08 r0 | git-submodule | https://github.com/tytso/pwgen.git |
| `quark` | 5ad0df9175 r0 | git-submodule | git://git.suckless.org/quark |
| `rc` | 1884d8fe62 | git-submodule | https://github.com/oasislinux/rc.git |
| `sdhcp` | 5f9956c870 r0 | git-submodule | https://github.com/michaelforney/sdhcp.git |
| `sfeed` | 2.4 r0 | git-submodule | git://git.codemadness.org/sfeed |
| `skeleton` | - | local | in-tree |
| `sndio` | 1.9.0 r1 | git-submodule | https://github.com/ratchov/sndio.git |
| `snes9x` | 32e556249e r0 | git-submodule | https://github.com/libretro/snes9x2010.git |
| `squashfs-tools-ng` | 1.1.3 r0 | git-submodule | https://github.com/AgentD/squashfs-tools-ng.git |
| `sshfs` | 3.6.0 r0 | git-submodule | https://github.com/libfuse/sshfs.git |
| `st` | c63a87cd93 r7 | git-submodule | git://git.suckless.org/st |
| `strace` | 6.19 r2 | tarball | https://github.com/strace/strace/releases/download/v6.19/strace-6.19.tar.xz |
| `swc` | 19893a5ca3 r0 | git-submodule | https://github.com/michaelforney/swc.git |
| `syslinux` | 6.03 r4 | tarball | https://www.kernel.org/pub/linux/utils/boot/syslinux/syslinux-6.03.tar.xz |
| `syslogd` | 4f40184d8a r0 | git-submodule | https://github.com/oasislinux/syslogd.git |
| `terminus-font` | 4.49.1 r0 | tarball | http://downloads.sourceforge.net/project/terminus-font/terminus-font-4.49/terminus-font-4.49.1.tar.gz |
| `texi2mdoc` | 0.1.2 r0 | tarball | http://mandoc.bsd.lv/texi2mdoc/snapshots/texi2mdoc-0.1.2.tgz |
| `the_silver_searcher` | 2.2.0 r3 | git-submodule | https://github.com/ggreer/the_silver_searcher.git |
| `tinyalsa` | 2.0.0-45-g4fbaeef r1 | git-submodule | https://github.com/tinyalsa/tinyalsa.git |
| `tinyemu` | 20191221 r2 | tarball | https://bellard.org/tinyemu/tinyemu-2019-12-21.tar.gz |
| `transmission` | 3.00 r3 | tarball | https://github.com/transmission/transmission-releases/raw/master/transmission-3.00.tar.xz |
| `tz` | 2026b | git-submodule | https://github.com/eggert/tz.git |
| `u-boot` | 2021.04 r3 | tarball | ftp://ftp.denx.de/pub/u-boot/u-boot-2021.04.tar.bz2 |
| `u-config` | 0.34.0 r1 | git-submodule | https://github.com/skeeto/u-config.git |
| `unbound` | 1.14.0 r0 | git-submodule | https://github.com/NLnetlabs/unbound.git |
| `usbids` | 2020.08.26 r0 | git-submodule | https://github.com/usbids/usbids.git |
| `util-linux` | 2.41.3 1 | tarball | https://www.kernel.org/pub/linux/utils/util-linux/v2.41/util-linux-2.41.3.tar.gz |
| `wayland-protocols` | 1.31 r0 | git-submodule | https://gitlab.freedesktop.org/wayland/wayland-protocols.git |
| `wireguard-tools` | 1.0.20260223 r1 | git-submodule | https://git.zx2c4.com/wireguard-tools |
| `wl9` | de70033524 r0 | git-submodule | https://git.sr.ht/~mcf/wl9 |
| `wld` | 3fe15e769c r0 | git-submodule | https://github.com/michaelforney/wld.git |
| `wpa_supplicant` | 2.11 r3 | tarball | http://w1.fi/releases/wpa_supplicant-2.11.tar.gz |
| `x509cert` | 0.4 r0 | git-submodule | https://git.sr.ht/~mcf/x509cert |
| `xkeyboard-config` | 2.36 r0 | git-submodule | https://gitlab.freedesktop.org/xkeyboard-config/xkeyboard-config.git |
| `yt-dlp` | 2026.10.21 r0 | tarball | https://github.com/yt-dlp/yt-dlp/releases/download/2026.10.21/yt-dlp.tar.gz |
| `zfs` | 2.4.0 r2 | tarball | https://github.com/openzfs/zfs/releases/download/zfs-2.4.0/zfs-2.4.0.tar.gz |
| `zlib` | 1.3.1 r0 | git-submodule | https://github.com/madler/zlib.git |
