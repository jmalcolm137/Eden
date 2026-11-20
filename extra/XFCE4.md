# Xfce 4 on Wayland

`extra/` carries a Wayland-only Xfce 4 desktop. The compositor is `xfwl4`;
there is no `xfwm4` and the compositor does not start XWayland. The Xfce
components have no X11 code path.

The two umbrella packages are:

| Package | Purpose |
|---|---|
| `xfce4-desktop` | The session: compositor, panel, desktop, settings, session, file manager, core apps and the default panel plugins |
| `xfce4-goodies` | The remaining applications, panel plugins and Thunar extensions |

Installing both gives the complete package set that is viable without X11.

## Versions

The core components use the 4.21 development series because `xfwl4` requires
`libxfce4ui` >= 4.21.4 (for `libxfce4kbd-private-3`) and `xfconf` >= 4.21.2:

```
libxfce4util   4.21.0     exo             4.21.0
xfconf         4.21.2     garcon          4.21.0
libxfce4ui     4.21.9     tumbler         4.21.1
libxfce4windowing 4.20.7  thunar          4.21.7
xfce4-panel    4.21.3     thunar-volman   4.20.0
xfce4-session  4.21.2     xfce4-settings  4.21.3
xfdesktop      4.21.1     xfce4-power-manager 4.21.1
xfce4-appfinder 4.21.1    xfwl4           4.21.1
```

Applications and panel plugins use their latest releases. Sources come from
`https://archive.xfce.org/src/`; every template carries the SHA-256 of the
upstream tarball.

## X11 is disabled

Every component that exposes a windowing switch is configured with:

```
-Dx11=disabled -Dwayland=enabled
```

In addition, the X11-only features are turned off explicitly:

```
libxfce4ui        -Dsession-management=disabled -Dstartup-notification=disabled
xfce4-panel       -Dgtk-layer-shell=enabled
xfce4-session     -Dlegacy-session-management=false -Dgtk-layer-shell=enabled
xfce4-settings    -Dlibxklavier=disabled -Dxcursor=disabled
                  -Dxorg-libinput=disabled -Dxrandr=disabled
xfce4-power-manager -Dpanel-plugin=enabled
xfwl4             --no-default-features
                  --features udev,egl,gettext-system,xwayland
```

`libxfce4ui` keeps `keyboard-library=true` because `xfwl4` and
`xfce4-settings` use `libxfce4kbd-private-3`.

`xfwl4` is compiled with its `xwayland` feature because the upstream shell
and focus code uses Smithay's XWayland types without gating every import, but
`post_patch` removes the `start_xwayland()` call from `main.rs`. No XWayland
binary is installed and the compositor never starts one.

The X11-only components are deliberately not packaged:

| Excluded | Reason |
|---|---|
| `xfwm4` | X11 window manager; `xfwl4` replaces it |
| `xfce4-xkb-plugin` | Requires libX11/libxklavier/libwnck |
| `xfce4-windowck-plugin` | Requires libX11/libwnck |
| `xfce4-screensaver` | X11 locking plus PAM authentication |
| `xfce4-volumed`, `xfce4-volumed-pulse` | X11 key grabs |
| `xfdashboard`, `orage` | X11 assumptions and unmaintained |
| `xfwm4-themes` art release | superseded by the theme-only package built from the `xfwm4` source |

`xfwm4-themes` is built from the `xfwm4` tarball but installs only
`/usr/share/themes`; no X11 code is compiled or installed.

## Package layout

Libraries and build tools:

```
libxfce4util libxfce4util-devel
xfconf xfconf-devel
libxfce4ui libxfce4ui-devel
libxfce4windowing libxfce4windowing-devel
exo exo-devel
garcon garcon-devel
tumbler tumbler-devel
xfce4-dev-tools
```

Core desktop:

```
xfwl4 xfce4-session xfce4-session-devel xfce4-settings xfce4-panel
xfdesktop xfce4-appfinder xfce4-power-manager thunar thunar-volman
xfwm4-themes xfce4-notifyd
```

Applications:

```
catfish gigolo mousepad parole ristretto xfburn xfce4-dict
xfce4-panel-profiles xfce4-screenshooter xfce4-taskmanager
xfce4-terminal
```

The Python applications use local 3.15 builds of `python-gobject`,
`python-dbus`, `python-pexpect`, `python-markupsafe`, `python-mako`,
`python-markdown`, `python-setuptools` and `python-pyyaml`; no prebuilt
Python modules are installed. `parole` uses the local `dbus-glib` package.

Panel plugins:

```
xfce4-battery-plugin xfce4-calculator-plugin xfce4-clipman-plugin
xfce4-cpufreq-plugin xfce4-cpugraph-plugin xfce4-diskperf-plugin
xfce4-docklike-plugin xfce4-eyes-plugin xfce4-fsguard-plugin
xfce4-generic-slider xfce4-genmon-plugin xfce4-mailwatch-plugin
xfce4-netload-plugin xfce4-places-plugin xfce4-pulseaudio-plugin xfce4-sensors-plugin
xfce4-smartbookmark-plugin xfce4-stopwatch-plugin
xfce4-systemload-plugin xfce4-time-out-plugin xfce4-timer-plugin
xfce4-verve-plugin xfce4-wavelan-plugin xfce4-weather-plugin
xfce4-whiskermenu-plugin
```

Thunar extensions:

```
thunar-archive-plugin thunar-media-tags-plugin thunar-vcs-plugin
```

`xfce4-mount-plugin` needs the BSD `fstab.h`/`getfsent()` API, which the
current musl base does not provide, so its template remains available but is
not part of either umbrella.

`xfce4-notes-plugin` now uses the real Meson package (`meson-real`) instead
of muon, which fixes its Vala build rules, but its Vala bindings also require
GObject-introspection GIR data. The local `glib` build has introspection
disabled, and `g-ir-scanner` currently crashes while generating the GLib GIR
under this toolchain, so the plugin is not in the umbrella yet.

## NetworkManager

`pkgsrc/networkmanager` provides the daemon, `nmcli` and `libnm`. It is built
without ModemManager, PPP, oFNM/oFono, Bluetooth DUN, teamd, OVS, eBPF,
SELinux, audit, systemd-journal, introspection, docs, `nmtui` and the wireless
extensions; crypto is GnuTLS and `nmcli` uses libedit. DHCP is the internal
client, and the daemon uses the keyfile plugin with `dns=default`.

The service is supervised by **perp**:

```
/etc/perp/networkmanager/rc
```

It runs `NetworkManager --no-daemon`. There is no `down` file, so
`perpboot` starts it by default; `perpctl` starts/stops it.

The GTK frontend is `network-manager-applet` (with `libnma` and `libsecret`),
added to the `xfce4-desktop` umbrella. It installs `/usr/bin/nm-applet` plus
its XDG autostart entry, and appears in the panel through the default
**Status Tray** plugin that `xfce4-panel` already ships in
`/etc/xdg/xfce4/panel/default.xml`. The applet is built without the
AppIndicator, WWAN and teamd options and with the unused `gdk/gdkx.h`
includes guarded for the X11-free GTK3 build.

## Toolkit stack

The Wayland-only toolkit closure now lives in `pkgsrc/` (the lower-level
libraries) and `extra/` (the GTK/Xfce layer), because `pkgsrc/` cannot depend
on `extra/`. The old static Oasis packages were upgraded in place, so there
are no duplicate X11 and Wayland variants of the same library:

| Layer | Packages |
|---|---|
| base | `glib` 2.90.1, `atk` 2.38.0 |
| text | `freetype` 2.14.3, `fontconfig` 2.18.3, `fribidi` 1.0.16, `harfbuzz` 14.5.0, `pango` 1.58.2 |
| image | `libpng` 1.6.59, `libjpeg-turbo` 2.0.6 (Oasis, with a local shared build), `gdk-pixbuf` 2.44.8 (builtin loaders) |
| 2D | `pixman` 0.46.4, `cairo` 1.18.6 |
| GL | `libglvnd` 1.7.0 (EGL/GLES only), `libepoxy` 1.5.10 (EGL only) |
| Wayland | `wayland` 1.26.0 (shared), `wayland-protocols` 1.49, `libxkbcommon` 1.13.2, `gtk-layer-shell` 0.10.1, `libdisplay-info` 0.3.0 |
| device | `libdrm` 2.4.134, `libinput` 1.31.3 |
| build | `bison` 3.8.2, `meson-real` 1.9.1, `pcre2` 10.49 |
| toolkit | `gtk+3` 3.24.43 with `-Dx11_backend=false -Dwayland_backend=true` |

Repository placement:

| Repo | Packages |
|---|---|
| `pkgsrc/` | `glib`, `pcre2`, `gdk-pixbuf`, `harfbuzz`, `atk`, `cairo`, `pango`, `gtk+3`, `gtk-layer-shell`, `libglvnd`, `libepoxy`, `libdisplay-info`, `meson-real` |
| `extra/` | Xfce libraries, applications and plugins, plus `gspell`, `gtksourceview4`, `libsoup3`, `vte-gtk3`, `fast_float`, `libseat`, `mesa`, `python-pyyaml`, `python-packaging` |

The X11 switches used throughout are:

```
glib        -Dselinux=disabled -Dlibmount=disabled -Dlibelf=disabled
cairo       -Dxlib=disabled -Dxcb=disabled -Dxlib-xcb=disabled
pango       -Dxft=disabled
gtk+3       -Dx11_backend=false -Dwayland_backend=true
libglvnd    -Dx11=disabled -Dglx=disabled -Degl=true
libepoxy    -Dx11=false -Dglx=no -Degl=yes
libxkbcommon -Denable-x11=false
```

`freetype` is built with `-Dharfbuzz=disabled` and `-Dpng=disabled` to keep
the font stack one-directional and the static consumers free of a libpng
dependency; `fontconfig` is the shared 2.18.3 build. `pixman`, `wayland`,
`wayland-protocols`, `libinput`, `freetype`, `fontconfig`, `fribidi`, `libdrm`,
`libpng`, `libexpat`, `gettext`, `libxml2`, `udev`, `autoconf`, `automake` and
`libtool` are the Oasis packages (the latter group ported from pkgsrc so the
toolkit has no downward dependencies). `pcre2` and `glib` live in `pkgsrc/`. `libxkbcommon` is back in `oasis/`: its
only `pkgsrc` edge was `bison`, which is avoided by building from the
bison-generated `parser.c`/`parser.h` tracked in `files/` (same approach as
the existing `files/xkbcommon.patch`), so no `bison` is needed at build time
and `bison` stays in `pkgsrc/` as required.

The upstream static archives for `wayland` and `pixman` do not include the
objects from their private helper libraries (`wayland-util`, `wayland-private`
and the SIMD implementations). Both templates fold those objects back into the
installed `.a` files in `post_build`, so the existing static Oasis consumers
keep working. Upstream also names the pixman archive `libpixman-1.a`, so
consumers link that path instead of the old `libpixman.a`.

Every library in the closure is now built from local source templates, with
no `main` or user repository. The added ports include:

| Area | Packages |
|---|---|
| support | `pcre2`, `libffi8` (core), `zlib`/`zlib-shared`, `libexpat`, `libpng`, `libjpeg-turbo`, `libtiff`, `hwdata`, `shared-mime-info`, `adwaita-icon-theme`, `xkeyboard-config`, `libyaml`, `libexif`, `json-c`, `icu`, `iso-codes`, `fast_float` |
| device | `udev`, `libgudev`, `libseat`, `mesa` (GBM/EGL), `libdisplay-info` |
| services | `libnotify`, `upower`, `polkit`, `libcanberra`, `sqlite`, `libsndfile`, `pulseaudio`/`libpulse` |
| network/TLS | `gmp`, `nettle`, `libtasn1`, `gnutls`, `glib-networking`, `nghttp2`, `libpsl`, `brotli`, `libssh2`, `libcurl`, `libsoup3` |
| apps | `vte-gtk3`, `gtksourceview4`, `gspell`, `enchant2`, `taglib`, `gstreamer`/`gst-plugins-base`, `libburn`, `libisofs` |

`rust`, `cargo`, `rust-bootstrap` and `cargo-bootstrap` are in `pkgsrc/`.
Rust cannot be built without a bootstrap compiler; `rust-bootstrap` and
`cargo-bootstrap` install the official Chimera stage0 binaries fetched as
checksummed distfiles. Everything else, including Rust 1.99.1 itself, is
compiled from source.

`bison` lives in `pkgsrc/`. `gdk-pixbuf` uses builtin PNG/JPEG/GIF loaders and an empty loaders cache
because the `gdk-pixbuf-query-loaders` tool crashes under the current musl
build; the image loaders themselves are compiled into the library.

`mesa` is now a local `extra/` port built Wayland-only (`-Dplatforms=wayland`,
`-Dglx=disabled`, no Vulkan) with the llvmpipe and softpipe drivers and
`gbm`/`egl`/`gles` enabled. The local `libglvnd` is EGL/GLES-only, so the GL
loader does not pull `libX11`.

`xfce4-dev-tools` carries a small `pre_configure` edit so its configure check
finds `muon` when looking for `meson`, matching this tree's engine mapping.

`tumbler` is built with the GStreamer, Poppler, GSF, libopenraw, FFmpeg and
cover thumbnailers disabled; the pixbuf, font and JPEG thumbnailers remain.
The cover thumbnailer needs `libcurl`; the other thumbnailers need libraries
that are still outside the X11-free closure.

## Testing

The stack was built in the `bldroot-oasis` created by
`tools/bootstrap-oasis.sh`: the Oasis toolkit, the ported dependency
libraries, the Xfce libraries, both umbrellas and `xfwl4`. The remote
repositories were removed before the final pass; only `core`, `oasis`,
`pkgsrc` and `extra` are configured. A final pass rebuilt all 51 packages
in the two umbrellas, `xfwl4`, `smithay`, the locally ported `libseat`,
`libinput`, `mesa` and `rust` with no remote repository.

`core/zlib-static` now also installs a shared `libz.so.1`, and
`core/base-cbuild` depends on it, because the local all-target LLVM used by
the Rust toolchain needs `libz` at load time. The bootstrap path needed small fixes in
`core/zlib-static` (pkgconf), `core/libressl` (pkgconf), `core/fakeroot`
(python, libcap, checks) and `core/xz` (no autotools regeneration).

The local LLVM bootstrap is X86-only, while the prebuilt Rust stage0 and the
Chimera LLVM package were built against an all-target LLVM. The Rust build
uses the all-target `libLLVM.so.22.1` in the test root; a bootstrap intended
for general Rust work should be built with `LLVM_TARGETS_TO_BUILD=all`.

`meson-real` provides upstream Meson for the templates that set
`meson_impl = "meson"`; everything else still uses muon. The Python
extensions are built against the tree's 3.15 interpreter, and `dbus-glib` is
built locally for Parole.

## Notes

- Upstream test suites need a display and a D-Bus session, so the templates
  set `!check`. Test the desktop in a real session instead.
- `xfconf`, `tumbler` and `thunar` install systemd user units; their
  templates remove them because this tree has no systemd.
- `xfce4-panel-profiles` and `catfish` are Python applications; `catfish`
  also needs a `locate` implementation at runtime.
- `thunar-archive-plugin` needs an archive manager (for example
  `file-roller`).
- `pavucontrol` is not ported: it needs the gtkmm-3 C++ stack. The
  `xfce4-pulseaudio-plugin` therefore has no mixer button target yet; its
  volume slider and mute controls work without it.
- `accountsservice` is not ported, so `xfce4-whiskermenu-plugin` is built
  with `-Daccountsservice=disabled` (no user avatar/account switching).
- `libqrencode` is not ported; `xfce4-clipman-plugin` is built with
  `-Dqrencode=disabled` (no QR code display).
- `lm-sensors` is not ported; `xfce4-sensors-plugin` is built with
  `-Dlibsensors=disabled` (ACPI/sysfs sensors only).
- `gnutls` is now local, so `xfce4-mailwatch-plugin` and
  `glib-networking` have TLS support.
- The `xfwl4` build consumes `extra/smithay`; keep the Smithay version in
  `extra/xfwl4/template.py` in sync with `extra/smithay/template.py`.
