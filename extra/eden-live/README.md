# Eden live ISO

## Boot

Kernel (`core/linux-kernel`, CachyOS 7.3.5, baseline x86-64 v1), limine and a
gzip cpio initramfs. `init.c` is PID 1; it mounts `devtmpfs`, `procfs`,
`sysfs`, tmpfs on `/run` and `/tmp`, starts `seatd`, the system D-Bus and
NetworkManager, then drops to uid 1000 (`action`) and starts the session bus,
`xfconfd` and `xfwl4 --backend tty --session xfce4-session`.

There is no login prompt: the session is started directly for `action`.

## Accounts

- `action` / `action` (uid 1000, home `/home/action`)
- `root` / `action`

## Packages

Assembled from the local `core`, `oasis`, `pkgsrc` and `extra` repositories:

- kernel/base: `linux-kernel`, `base-kernel`, `kmod`, `base-cbuild` deps
- X11: `xwayland`, `libx11`, `libxcb`, `libxau`, `libxdmcp`, `libxfont2`,
  `libfontenc`, `libxkbfile`, `libxcvt`, `libxshmfence`, `libtirpc`,
  `xorgproto`, `xtrans`, `xorg-util-macros`, `xcbproto`,
  `xserver-xorg-protocol`
- desktop: `xfwl4`, `xfce4-session`, `xfce4-panel`, `xfdesktop`, `thunar`,
  `xfconf`, `gtk3`, `mesa` (llvmpipe), `adwaita-icon-theme`, fonts
- network: `networkmanager`, `wpa_supplicant`, `libnma`, `nm-applet`

`xfconfd-lite` (this directory, `extra/xfconfd-lite`) provides the session
`org.xfce.Xfconf` service used by the Xfce components.

## Building

`mkiso.sh` compiles `init.c` against the musl build root, packs `$ROOT`
(default `/tmp/eden-root`) and writes `$OUT` (default `/tmp/eden-live.iso`).

## Known limitations

- QEMU's `bochs`/`std` VGA only exposes a software EGL device; `xfwl4` is
  patched to accept it (llvmpipe) and renders slowly.
- No cursor theme is installed, so the pointer is invisible and bitmap
  cursors fall back to a blank image (the retry log is at debug level).
- `xfwm4` and `xfce4-settings` are not packaged yet, so the session has no
  window manager and no settings daemon. `xfdesktop` currently aborts in
  `g_file_icon_constructed()`; the panel does start.
- NetworkManager runs with Wi-Fi enabled, but QEMU provides no wireless
  interface and no credentials/SSID are baked into the image.
