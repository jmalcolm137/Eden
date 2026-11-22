# COSMIC on Eden

`extra/` carries the COSMIC desktop from System76.  The upstream components
are Rust programs built against the Wayland stack already used by the Xfce
packages.

There is **no login manager**.  `cosmic-greeter` is deliberately not packaged.
The session is started from a TTY.

## Starting from a TTY

Log in on a virtual console and run:

```
start-cosmic
```

`start-cosmic` creates `XDG_RUNTIME_DIR` when the TTY login did not, starts a
private session bus with `dbus-run-session`, and execs `cosmic-session`.
`cosmic-session` then starts the compositor, panel, applets and the rest of the
session.

## systemd to perp

Upstream ships a systemd user session: `cosmic-session.target` binds
`cosmic-comp.service`, and several components use `systemctl --user` to import
the environment and create scopes.  Eden has no systemd user manager.  The
port is:

| Upstream | Eden |
|---|---|
| `cosmic-session.target`, `cosmic-comp.service` | perp service `/etc/perp/cosmic-session` |
| `systemctl --user import-environment` | environment is exported by `start-cosmic` and the perp `rc.main` |
| `systemctl --user set-environment` | removed; `cosmic-session` is built without the `systemd` feature |
| systemd scopes for launched apps | `cosmic-session`'s own launch-pad process manager |
| logind seat/VT handling | `seatd` plus `libseat`; `cosmic-comp` is built without the `logind` feature |
| journald logging | tracing subscriber on stderr |
| PipeWire systemd user socket activation | per-user perp service via `pipewire-perp` and the COSMIC autostart entry |
| portal/user units | D-Bus activation; units are not installed |

The `systemd` and `logind` Cargo features are disabled when building
`cosmic-session` and `cosmic-comp`, so the binaries do not try to talk to
systemd at runtime.  The freedesktop autostart support is kept: when the
session manager does not detect systemd it runs the `XDG_CONFIG_DIRS/autostart`
entries itself.

The perp service replaces the systemd user target for systems that want the
desktop started automatically (for example a dedicated seat):

```
/etc/perp/cosmic-session/rc.main
```

It waits for `seatd` and the udev coldplug pass, prepares the user's
`XDG_RUNTIME_DIR`, and runs `start-cosmic` as `$COSMIC_USER` (default
`action`, the Eden live user).  The directory carries the sticky bit that
marks a perp service as active.

## Packages

Libraries and data:

```
cosmic-icons cosmic-wallpapers cosmic-sound-theme
```

Session:

```
cosmic-session cosmic-comp cosmic-panel cosmic-applets
cosmic-launcher cosmic-app-library cosmic-workspaces cosmic-osd
cosmic-notifications cosmic-bg cosmic-idle
cosmic-settings cosmic-settings-daemon cosmic-randr xdg-desktop-portal wireplumber
```

Applications:

```
cosmic-files cosmic-term cosmic-edit cosmic-store
cosmic-screenshot cosmic-player cosmic-viewer cosmic-monitor
```

Umbrella: `cosmic-desktop`.
