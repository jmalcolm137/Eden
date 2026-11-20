# Eden live ISO

## Boot

Kernel (`core/linux-kernel`, CachyOS 7.3.5, baseline x86-64 v1) and limine on
a hybrid ISO (BIOS El Torito plus a FAT EFI system partition).

The initramfs is small: a static `liveinit` plus the storage and filesystem
modules required to find the ISO (`sr_mod`, `usb-storage`, `nvme`, `isofs`,
`loop`, `squashfs`, `overlay`, ...). `liveinit` mounts the ISO, loop-mounts
`/eden/rootfs.squashfs`, builds a tmpfs-backed overlay for writes and
`pivot_root`s into it. The squashfs root stays on the ISO and is read on
demand, so the image booted with 512 MB RAM in both BIOS and UEFI tests.

After the switch, `sinit` is PID 1. It runs `/etc/rc.init`, which mounts
`devpts` and tmpfs on `/tmp` and `/dev/shm`, sets the hostname, prepares the
runtime directories and the session user's home, runs a coldplug pass over
`/sys/bus/*/devices/*/modalias` and loads `mac80211_hwsim radios=2`. It then
hands the system to `perpd /etc/perp`; `sinit` stays PID 1 and reaps orphans
while `perp` supervises the long-running daemons. A small static helper
(`extra/eden-live/hotplug.c`) provides the coldplug pass and a netlink uevent
listener so kernel modules load without udev.

The perp services (directories under `/etc/perp`, activated by the sticky bit)
are:

- `dbus` - system bus
- `seatd` - seat and device access for the compositor
- `hotplug` - the uevent listener
- `wpa_supplicant` - global D-Bus control interface
- `hostapd` - open demo AP `eden-test` on `wlan1`
- `networkmanager` - NetworkManager plus the udev-less link poke
- `session` - `runuid action` starts the session bus, `xfconfd` and
  `xfwl4 --backend tty --session /usr/local/bin/eden-session`
- `console` - root shell on `ttyS0`

`wlan0` is left to NetworkManager, which autoconnects it to `eden-test` with
the stored profile; `eth0` comes up through DHCP as usual. This exercises the
complete real path (netlink, `wpa_supplicant` D-Bus, NetworkManager device
plugins) even in QEMU, which has no 802.11 hardware.

There is no login prompt: the `session` service starts directly for `action`.

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

- kernel/base: `linux-kernel`, `base-kernel`, `kmod`, `sinit`, `perp`,
  `base-cbuild` deps
- X11 libraries used by the Wayland clients: `libx11`, `libxcb`, ...
  (`xwayland` is built but unused)
- desktop: `xfwl4`, `xfce4-panel`, `xfdesktop`, `thunar`, `xfconf`,
  `gtk3`, `mesa` (llvmpipe), `adwaita-icon-theme`, fonts
- network: `networkmanager`, `wpa_supplicant`, `hostapd` (demo AP)
- tools: `htop` (static-pie, built against `netbsd-curses`), `xfce4-terminal`

`xfconfd-lite` (`extra/xfconfd-lite`) provides the session
`org.xfce.Xfconf` service.

## Build

`mkiso.sh` builds `/eden/rootfs.squashfs` from `$ROOT` (default
`/tmp/eden-root`) with `mksquashfs -all-root`, compiles `liveinit` and the
hotplug helper against the musl build root, assembles the initramfs module
list (`mkinitramfs.py`), creates the FAT ESP with `mkfs.vfat`/mtools and
writes a hybrid BIOS/UEFI ISO to `$OUT` (default `/tmp/eden-live.iso`).
Host tools required: `mksquashfs`, `zstd`, `mkfs.vfat`, `mmd`, `mcopy`.

## Fixes worth knowing

- `glib` must be built with `-Ddefault_library=shared`; otherwise `libgio`
  statically embeds `libgobject`/`libglib`, creating a second GObject type
  system in every process (random property failures, crashes, GVariant
  assertions).
- Package triggers are skipped when assembling with `apk --no-scripts`, so
  `mime.cache`, `gschemas.compiled` and icon caches must be generated
  explicitly (`mkiso.sh` does this).
- NetworkManager is patched to clear `NM_UNMANAGED_PLATFORM_INIT` without a
  udev event; combined with the `rc.init` coldplug, the hotplug service and
  the link poke this lets it manage devices on a udev-less live image.
- NetworkManager refuses to load device plugins whose files are not owned by
  root. The squashfs is built with `-all-root` for this reason.
- Desktop output goes to `/run/user/1000/eden-session.log` so it does not
  flood the serial console.

## Known limitations

- The WiFi path is demonstrated with `mac80211_hwsim` and a local `hostapd`
  AP. With a real wireless NIC the driver loads through the uevent helper
  and NetworkManager uses the same `wpa_supplicant` backend; only the
  network profile (SSID/credentials) needs to be provided.
- llvmpipe rendering is slow; no hardware EGL device is required, `xfwl4`
  is patched to accept software devices.
- No cursor theme is installed, so the pointer is invisible.
