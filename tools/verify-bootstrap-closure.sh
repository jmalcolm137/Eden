#!/bin/sh
# Verify the local Oasis-composed cbuild template set.
#
# Checks:
#   1. manifest is sorted, unique, and every entry has main/<name>/template.py
#   2. main/ contains no templates outside the manifest
#   3. every subpackage symlink points at a manifest template
#   4. every local template parses and lints
#   5. the composed base-cbuild has the intended Oasis/Chimera split
#   6. base-files carries the account files cbuild reads

set -eu

here=$(CDPATH= cd -- "$(dirname -- "$0")/.." && pwd)
manifest="$here/bootstrap-packages.txt"
cd "$here"

fail=0

tmp="$here/.tmp.verify.$$"
cleanup() {
    rm -rf "$tmp"
}
trap cleanup EXIT INT TERM

mkdir -p "$tmp"

grep -v '^[[:space:]]*\(#\|$\)' "$manifest" | sort > "$tmp/manifest"

if ! sort -c "$tmp/manifest" 2>/dev/null; then
    echo "error: manifest is not sorted" >&2
    fail=1
fi

if uniq -d "$tmp/manifest" | grep -q .; then
    echo "error: manifest contains duplicate entries:" >&2
    uniq -d "$tmp/manifest" >&2
    fail=1
fi

while IFS= read -r p; do
    if [ ! -f "main/$p/template.py" ]; then
        echo "error: missing template directory: main/$p" >&2
        fail=1
    fi
done < "$tmp/manifest"

for el in main/*; do
    [ -e "$el" ] || [ -L "$el" ] || continue

    base=${el#main/}

    if [ -L "$el" ]; then
        target=$(readlink "$el")
        if ! grep -qxF "$target" "$tmp/manifest"; then
            echo "error: subpackage symlink $el -> $target does not point" \
                "at a manifest template" >&2
            fail=1
        fi
        continue
    fi

    if [ ! -d "$el" ]; then
        echo "error: unexpected file in main/: $el" >&2
        fail=1
        continue
    fi

    if [ ! -f "$el/template.py" ]; then
        echo "error: directory without template.py: $el" >&2
        fail=1
        continue
    fi

    if ! grep -qxF "$base" "$tmp/manifest"; then
        echo "error: template not in manifest: main/$base" >&2
        fail=1
    fi
done

# Parse every local template.
if ! ./cbuild dump > /dev/null; then
    echo "error: cbuild failed to parse the local template tree" >&2
    fail=1
fi

# Lint the local set.
while IFS= read -r p; do
    if ! ./cbuild lint "main/$p" > /dev/null 2>&1; then
        echo "error: lint failed: main/$p" >&2
        fail=1
    fi
done < "$tmp/manifest"

# Composition checks: Oasis userland in, Chimera base userland out.
for p in linux-personality oksh pigz sbase ubase gmake; do
    if ! grep -q "\"$p\"" main/base-cbuild/template.py; then
        echo "error: base-cbuild does not depend on $p" >&2
        fail=1
    fi
done

for p in chimerautils chimerautils-extra ccache; do
    if grep -q "\"$p\"" main/base-cbuild/template.py; then
        echo "error: base-cbuild still depends on $p" >&2
        fail=1
    fi
done

# The local gmake must not install /usr/bin/make; sbase owns that name.
if grep -q 'install_link("usr/bin/gmake", "make")' main/gmake/template.py; then
    echo "error: local gmake would overwrite the Oasis /usr/bin/make" >&2
    fail=1
fi
if ! grep -q 'rename("usr/bin/make", "usr/bin/gmake"' \
        main/gmake/template.py; then
    echo "error: local gmake does not rename make to gmake" >&2
    fail=1
fi

# cbuild must invoke gmake, not the Oasis make.
if ! grep -q '("make_cmd", "gmake"' src/cbuild/core/template.py; then
    echo "error: cbuild make_cmd is not gmake" >&2
    fail=1
fi

for f in main/base-files/files/etc/passwd main/base-files/files/etc/group; do
    if [ ! -f "$f" ]; then
        echo "error: missing account file: $f" >&2
        fail=1
    fi
done

if [ -f bldroot/.cbuild_chroot_init ]; then
    echo "note: bldroot exists"
else
    echo "note: no bldroot; run tools/bootstrap.sh" \
        "(temporary Chimera root) or tools/bootstrap-oasis.sh"
fi

if [ "$fail" -ne 0 ]; then
    exit 1
fi

echo "ok: $(wc -l < "$tmp/manifest") local templates;" \
    "Oasis-composed base-cbuild is consistent"
