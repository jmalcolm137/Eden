#!/bin/sh
# Verify the self-hosting package list and the local template tree.
#
# Checks:
#   1. manifest is sorted, unique, and every entry has main/<name>/template.py
#   2. main/ contains no templates outside the manifest
#   3. every subpackage symlink points at a manifest template
#   4. every local template parses and lints
#   5. bldroot is present and carries base-cbuild (informational)
#
# This verifier does not contact the network and does not rebuild anything.

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

# Parse every local template (also catches broken imports).
if ! ./cbuild dump > /dev/null; then
    echo "error: cbuild failed to parse the local template tree" >&2
    fail=1
fi

# The local graph must be exactly the source-bootstrap closure. This also
# catches the stage-3 ccache branch (and its boost/util-linux tree) coming
# back, e.g. if the local base-cbuild patch was not applied.
if ./cbuild print-build-graph main/base-cbuild \
        | sed 's/^ *//' \
        | sort -u > "$tmp/graph"; then
    if ! diff -u "$tmp/manifest" "$tmp/graph"; then
        echo "error: local build graph does not match the manifest" >&2
        fail=1
    fi
else
    echo "error: cbuild failed to produce the bootstrap build graph" >&2
    fail=1
fi

# Lint the self-hosting set itself.
while IFS= read -r p; do
    if ! ./cbuild lint "main/$p" > /dev/null 2>&1; then
        echo "error: lint failed: main/$p" >&2
        fail=1
    fi
done < "$tmp/manifest"

if [ -f bldroot/.cbuild_chroot_init ]; then
    if [ -x bldroot/usr/bin/apk.static ]; then
        barch=$(cat bldroot/.cbuild_chroot_init)
        if bldroot/usr/bin/apk.static --root bldroot --arch "$barch" \
                info base-cbuild > /dev/null 2>&1; then
            :
        else
            echo "warning: bldroot exists but base-cbuild is not installed" >&2
        fi
    fi
else
    echo "note: no bldroot; run ./cbuild source-bootstrap" \
        "(or tools/bootstrap.sh for the binary shortcut)"
fi

if [ "$fail" -ne 0 ]; then
    exit 1
fi

echo "ok: $(wc -l < "$tmp/manifest") source templates;" \
    "source-bootstrap graph matches manifest"
