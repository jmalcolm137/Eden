#!/bin/sh
# Build eden-oasis.iso: sinit/perp + OASIS packages + velox/st, squashfs root on
# the ISO, small initramfs, limine for BIOS and UEFI.
set -eu

repo=$(cd "$(dirname "$0")/../.." && pwd)
here=$(dirname "$0")
root=${ROOT:-$repo/oasis-root}
iso=${ISO:-$repo/oasis-iso}
name=${NAME:-eden-oasis}
out=${OUT:-$repo/$name.iso}
bldroot=${BLDROOT:-$repo/bldroot-oasis}
bootsrc=${BOOTSRC:-/tmp/eden-iso/boot}

for t in mksquashfs zstd mkfs.vfat mmd mcopy; do
    command -v "$t" >/dev/null || {
        echo "missing host tool: $t" >&2
        exit 1
    }
done
[ -x "$root/usr/bin/sinit" ] || {
    echo "missing $root/usr/bin/sinit" >&2
    exit 1
}
[ -d "$root/etc/perp/velox" ] || {
    echo "missing perp configuration in $root" >&2
    exit 1
}
[ -e "$bootsrc/vmlinuz" ] || {
    echo "missing kernel at $bootsrc/vmlinuz" >&2
    exit 1
}

# 1. squashfs root
rm -rf "$iso"
mkdir -p "$iso/boot" "$iso/eden"
cp -a "$bootsrc"/. "$iso/boot"/
install -Dm644 "$repo/extra/boot/limine.conf" "$iso/boot/limine/limine.conf"
rm -f "$iso/boot/initramfs.gz"
mksquashfs "$root" "$iso/eden/rootfs.squashfs" -noappend -no-progress \
    -all-root -comp zstd -Xcompression-level 19

# 2. static liveinit
cp "$repo/extra/eden-live/liveinit.c" /tmp/oasis-liveinit.c
bwrap --unshare-all --hostname cbuild \
    --ro-bind "$bldroot" / \
    --bind /tmp /builddir \
    --dev /dev --proc /proc --tmpfs /run --tmpfs /tmp \
    --new-session --die-with-parent --uid 0 --gid 0 --chdir /builddir \
    -- /bin/sh -c "/usr/bin/clang -O2 -static-pie -unwindlib=none \
        -o /builddir/oasis-liveinit /builddir/oasis-liveinit.c"

# 3. initramfs: liveinit + storage/filesystem modules
stage=/tmp/oasis-initramfs
rm -rf "$stage"
mkdir -p "$stage"
install -m755 /tmp/oasis-liveinit "$stage/init"
python3 "$repo/extra/eden-live/mkinitramfs.py" "$root" "$stage"
( cd "$stage" && find . | cpio -o -H newc -R 0:0 2>/dev/null | gzip -9 ) \
    > "$iso/boot/initramfs.gz"

# 4. UEFI ESP image
efi="$iso/boot/limine/efi.img"
rm -f "$efi"
dd if=/dev/zero of="$efi" bs=1M count=16 status=none
label=$(echo "$name" | tr a-z A-Z | tr -d "-" | cut -c1-11)
mkfs.vfat -F 16 -n "$label" "$efi" >/dev/null
mmd -i "$efi" ::/EFI ::/EFI/BOOT
mcopy -i "$efi" "$iso/boot/limine/EFI/BOOT/BOOTX64.EFI" \
    ::/EFI/BOOT/BOOTX64.EFI

# 5. hybrid ISO with limine
rm -f "$out"
xorriso -as mkisofs \
    -V "$(echo "$name" | tr a-z A-Z)" \
    -b boot/limine/limine-bios-cd.bin -no-emul-boot -boot-load-size 4 \
    -boot-info-table \
    --efi-boot boot/limine/efi.img -no-emul-boot \
    --efi-boot-part --efi-boot-image --protective-msdos-label \
    "$iso" -o "$out"

echo "wrote $out"
