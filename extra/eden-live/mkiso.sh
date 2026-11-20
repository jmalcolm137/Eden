#!/bin/sh
# Build the Eden live ISO: installs sinit as PID 1 with a perp service tree,
# compiles the hotplug helper in a musl build root, installs the Wayland
# session defaults, packs the image root as a gzip cpio initramfs and wraps
# kernel + initramfs with limine.
set -eu

repo=$(cd "$(dirname "$0")/../.." && pwd)
here=$(dirname "$0")
root=${ROOT:-/tmp/eden-root}
iso=${ISO:-/tmp/eden-iso}
out=${OUT:-/tmp/eden-live.iso}
bldroot=${BLDROOT:-$repo/bldroot-oasis}

if [ ! -x "$bldroot/usr/bin/clang" ]; then
    echo "missing musl/clang build root at $bldroot" >&2
    exit 1
fi

# 1. sinit is PID 1; /etc/rc.init prepares the root and execs perpd
[ -x "$root/usr/bin/sinit" ] || {
    echo "missing $root/usr/bin/sinit (install the sinit package first)" >&2
    exit 1
}
install -m755 "$root/usr/bin/sinit" "$root/init"
install -Dm755 "$here/rc.init" "$root/etc/rc.init"
install -Dm755 "$here/rc.shutdown" "$root/etc/rc.shutdown"

# udev-less coldplug/uevent helper (static-pie)
cp "$here/hotplug.c" /tmp/eden-live-hotplug.c
bwrap --unshare-all --hostname cbuild \
    --ro-bind "$bldroot" / \
    --bind /tmp /builddir \
    --dev /dev --proc /proc --tmpfs /run --tmpfs /tmp \
    --new-session --die-with-parent --uid 0 --gid 0 --chdir /builddir \
    -- /bin/sh -c "/usr/bin/clang -O2 -static-pie -unwindlib=none \
        -o /builddir/eden-hotplug /builddir/eden-live-hotplug.c"
install -Dm755 /tmp/eden-hotplug "$root/usr/local/bin/eden-hotplug"

# perp service tree; the sticky bit marks a service as active
for svc in "$here"/perp/*; do
    name=$(basename "$svc")
    install -Dm755 "$svc/rc.main" "$root/etc/perp/$name/rc.main"
    chmod 1755 "$root/etc/perp/$name"
done

install -Dm755 "$here/files/eden-session-start" "$root/usr/local/bin/eden-session-start"
install -Dm755 "$here/files/eden-netpoke" "$root/usr/local/bin/eden-netpoke"

# 2. session defaults (Wayland only; no X11 session manager)
install -Dm755 "$here/files/eden-session" "$root/usr/local/bin/eden-session"
install -Dm644 "$here/files/eden.png" "$root/usr/share/backgrounds/eden.png"
install -Dm644 "$here/files/xfce4-panel.xml" \
    "$root/etc/xdg/xfce4/xfconf/xfce-perchannel-xml/xfce4-panel.xml"
install -Dm644 "$here/files/xfce4-desktop.xml" \
    "$root/etc/xdg/xfce4/xfconf/xfce-perchannel-xml/xfce4-desktop.xml"

# simulated 802.11 network for the live image (mac80211_hwsim)
install -Dm644 "$here/files/ibss-eden.conf" \
    "$root/etc/wpa_supplicant/ibss-eden.conf"
install -Dm600 "$here/files/eden-test.nmconnection" \
    "$root/etc/NetworkManager/system-connections/eden-test.nmconnection"
install -Dm644 "$here/files/99-live.conf" \
    "$root/etc/NetworkManager/conf.d/99-live.conf"
install -Dm644 "$here/files/eden.conf" "$root/etc/hostapd/eden.conf"

# 3. caches that package triggers normally generate (we install with --no-scripts)
bwrap --unshare-all --hostname eden --bind "$root" / \
    --dev /dev --proc /proc --tmpfs /run --tmpfs /tmp \
    --new-session --die-with-parent --uid 0 --gid 0 --chdir / \
    -- /bin/sh -c '
        [ -x /usr/bin/update-mime-database ] && update-mime-database /usr/share/mime || true
        [ -x /usr/bin/glib-compile-schemas ] && glib-compile-schemas /usr/share/glib-2.0/schemas || true
        for t in Adwaita AdwaitaLegacy hicolor; do
            [ -d /usr/share/icons/$t ] && gtk-update-icon-cache -f -t /usr/share/icons/$t || true
        done
    '

# 4. initramfs
( cd "$root" && find . | cpio -o -H newc -R 0:0 2>/dev/null | gzip -1 ) \
    > "$iso/boot/initramfs.gz"

# 5. ISO
rm -f "$out"
xorriso -as mkisofs \
    -b boot/limine/limine-bios-cd.bin -no-emul-boot -boot-load-size 4 \
    -boot-info-table \
    --efi-boot boot/limine/EFI/BOOT/BOOTX64.EFI \
    --efi-boot-part --efi-boot-image --protective-msdos-label \
    "$iso" -o "$out"

echo "wrote $out"
