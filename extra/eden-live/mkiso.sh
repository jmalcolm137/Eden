#!/bin/sh
# Build the Eden live ISO: compiles the init in a musl build root, installs the
# Wayland session defaults, packs the image root as a gzip cpio initramfs and
# wraps kernel + initramfs with limine.
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

# 1. init (static-pie, PID 1)
cp "$here/init.c" /tmp/eden-live-init.c
bwrap --unshare-all --hostname cbuild \
    --ro-bind "$bldroot" / \
    --bind /tmp /builddir \
    --dev /dev --proc /proc --tmpfs /run --tmpfs /tmp \
    --new-session --die-with-parent --uid 0 --gid 0 --chdir /builddir \
    -- /bin/sh -c "/usr/bin/clang -O2 -static-pie -unwindlib=none \
        -o /builddir/eden-init /builddir/eden-live-init.c"
install -m755 /tmp/eden-init "$root/init"

# 2. session defaults (Wayland only; no X11 session manager)
install -Dm755 "$here/files/eden-session" "$root/usr/local/bin/eden-session"
install -Dm644 "$here/files/eden.png" "$root/usr/share/backgrounds/eden.png"
install -Dm644 "$here/files/xfce4-panel.xml" \
    "$root/etc/xdg/xfce4/xfconf/xfce-perchannel-xml/xfce4-panel.xml"
install -Dm644 "$here/files/xfce4-desktop.xml" \
    "$root/etc/xdg/xfce4/xfconf/xfce-perchannel-xml/xfce4-desktop.xml"

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
