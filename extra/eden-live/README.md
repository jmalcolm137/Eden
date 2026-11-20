# Eden live ISO

## Boot

Kernel (`core/linux-kernel`, CachyOS 7.3.5, baseline x86-64 v1), limine and a
gzip cpio initramfs. `init.c` is PID 1: it mounts `devtmpfs`, `procfs`,
`sysfs`, tmpfs on `/run` and `/tmp`, runs a coldplug pass over
`/sys/bus/*/devices/*/modalias` and then keeps a netlink uevent listener so
kernel modules load without udev.

It starts `seatd`, the system D-Bus and NetworkManager, pokes existing network
links so NetworkManager picks them up, then drops to uid 1000 (`action`) and
starts the session bus, `xfconfd` and `xfwl4 --backend tty --session
/usr/local/bin/eden-session`.

There is no login prompt: the session starts directly for `action`.
`sinit` and `perp` are packaged in the tree, but this image still uses the
custom init; moving to sinit as PID 1 and perp services is the next step.

## Session: Wayland only

The desktop is 100% Wayland and does not use X11 or Xwayland at all:

- `xfwl4` is the compositor (tty/udev backend).
- `xfce4-panel` is built with `-Dx11=disabled -Dwayland=enabled`.
- `xfdesktop` (Wayland support via libxfce4windowing) and `thunar --daemon`
  are started directly by `eden-session`.
- `xfce4-session`, `xfwm4` and Xwayland are not run.

## Accounts

- `action` / `action` (uid 1000, home `/home/action`)
- `root` / `action`

## Packages

Assembled from the local `core`, `oasis`, `pkgsrc` and `extra` repositories:

- kernel/base: `linux-kernel`, `base-kernel`, `kmod`, `base-cbuild` deps
- X11 libraries used by the Wayland clients: `libx11`, `libxcb`, ...
  (`xwayland` is built but unused)
- desktop: `xfwl4`, `xfce4-panel`, `xfdesktop`, `thunar`, `xfconf`,
  `gtk3`, `mesa` (llvmpipe), `adwaita-icon-theme`, fonts
- network: `networkmanager`, `wpa_supplicant`

`xfconfd-lite` (`extra/xfconfd-lite`) provides the session
`org.xfce.Xfconf` service.

## Build

`mkiso.sh` compiles `init.c` against the musl build root, installs the
session defaults, generates the mime/schema/icon caches, packs `$ROOT`
(default `/tmp/eden-root`) and writes `$OUT` (default `/tmp/eden-live.iso`).

## Fixes worth knowing

- `glib` must be built with `-Ddefault_library=shared`; otherwise `libgio`
  statically embeds `libgobject`/`libglib`, creating a second GObject type
  system in every process (random property failures, crashes, GVariant
  assertions).
- Package triggers are skipped when assembling with `apk --no-scripts`, so
  `mime.cache`, `gschemas.compiled` and icon caches must be generated
  explicitly (`mkiso.sh` does this).
- NetworkManager is patched to clear `NM_UNMANAGED_PLATFORM_INIT` without a
  udev event; combined with the init coldplug/hotplug and link pokes this
  lets it manage devices on a udev-less live image.

## Known limitations

- QEMU has no 802.11 emulation, so Wi-Fi association cannot be exercised
  there. With a real wireless NIC the driver loads through the uevent
  helper and NetworkManager uses `wpa_supplicant` (the default backend).
- llvmpipe rendering is slow; no hardware EGL device is required, `xfwl4`
  is patched to accept software devices.
- No cursor theme is installed, so the pointer is invisible.
