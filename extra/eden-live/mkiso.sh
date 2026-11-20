#!/bin/sh
# Build the Eden live ISO: compiles the init in a musl build root, packs the
# image root as a gzip cpio initramfs and wraps kernel + initramfs with limine.
set -eu

repo=$(cd "$(dirname "$0")/../.." && pwd)
root=${ROOT:-/tmp/eden-root}
iso=${ISO:-/tmp/eden-iso}
out=${OUT:-/tmp/eden-live.iso}
bldroot=${BLDROOT:-$repo/bldroot-oasis}

if [ ! -x "$bldroot/usr/bin/clang" ]; then
    echo "missing musl/clang build root at $bldroot" >&2
    exit 1
fi

# 1. init (static-pie, own reaper and service supervision)
bwrap --unshare-all --hostname cbuild \
    --ro-bind "$bldroot" / \
    --bind /tmp /builddir \
    --dev /dev --proc /proc --tmpfs /run --tmpfs /tmp \
    --new-session --die-with-parent --uid 0 --gid 0 --chdir /builddir \
    -- /bin/sh -c "/usr/bin/clang -O2 -static-pie -unwindlib=none \
        -o /builddir/eden-init /builddir/eden-live-init.c"
install -m755 /tmp/eden-init "$root/init"

# 2. initramfs
( cd "$root" && find . | cpio -o -H newc -R 0:0 2>/dev/null | gzip -1 ) \
    > "$iso/boot/initramfs.gz"

# 3. ISO
rm -f "$out"
xorriso -as mkisofs \
    -b boot/limine/limine-bios-cd.bin -no-emul-boot -boot-load-size 4 \
    -boot-info-table \
    --efi-boot boot/limine/EFI/BOOT/BOOTX64.EFI \
    --efi-boot-part --efi-boot-image --protective-msdos-label \
    "$iso" -o "$out"

echo "wrote $out"
