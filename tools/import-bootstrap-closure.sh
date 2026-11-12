#!/bin/sh
# Import the cbuild engine and the source-bootstrap template set from an
# existing cports checkout.
#
# This only ever writes inside this tree. The upstream checkout is read-only.
#
# Usage:
#   tools/import-bootstrap-closure.sh [/path/to/cports]
#
# The default upstream path is ../cports relative to this tree.

set -eu

here=$(CDPATH= cd -- "$(dirname -- "$0")/.." && pwd)
upstream=${1:-"$here/../cports"}
manifest="$here/bootstrap-packages.txt"

if [ ! -x "$upstream/cbuild" ] || [ ! -d "$upstream/main" ]; then
    echo "error: '$upstream' does not look like a cports checkout" >&2
    exit 1
fi

if [ ! -f "$manifest" ]; then
    echo "error: missing manifest: $manifest" >&2
    exit 1
fi

echo "importing cbuild engine from $upstream"

install -m 0755 "$upstream/cbuild" "$here/cbuild"

rm -rf "$here/src"
cp -a "$upstream/src" "$here/src"
find "$here/src" -type d -name __pycache__ -prune -exec rm -rf {} +

mkdir -p "$here/etc"
rm -rf "$here/etc/build_profiles"
cp -a "$upstream/etc/build_profiles" "$here/etc/build_profiles"
cp -a "$upstream/etc/config.ini.example" "$here/etc/config.ini.example"

# Repository definitions and Chimera signing keys are needed both for a
# binary bootstrap and for resolving remote dependencies.
rm -rf "$here/etc/apk"
cp -a "$upstream/etc/apk" "$here/etc/apk"

if [ -f "$upstream/COPYING.md" ]; then
    cp -a "$upstream/COPYING.md" "$here/COPYING.md"
fi
if [ -f "$upstream/.flake8" ]; then
    cp -a "$upstream/.flake8" "$here/.flake8"
fi
if [ -f "$upstream/pyproject.toml" ]; then
    cp -a "$upstream/pyproject.toml" "$here/pyproject.toml"
fi

count=$(grep -cv '^[[:space:]]*\(#\|$\)' "$manifest" || true)
echo "importing $count template directories"

mkdir -p "$here/main"

# main/ is a generated import target. Clear it, then copy exactly the
# manifest; this prunes templates from a previous, larger import.
find "$here/main" -mindepth 1 -maxdepth 1 -exec rm -rf -- {} +

while IFS= read -r p; do
    [ -n "$p" ] || continue
    case "$p" in
        \#*) continue ;;
    esac

    if [ ! -f "$upstream/main/$p/template.py" ]; then
        echo "error: missing upstream template: main/$p" >&2
        exit 1
    fi

    rm -rf "$here/main/$p"
    # -L so that patch symlinks into sibling directories (e.g.
    # libusb-bootstrap/patches -> ../libusb/patches) are materialized
    # instead of becoming dangling links.
    cp -aL "$upstream/main/$p" "$here/main/$p"
done < "$manifest"

if [ "$count" -eq 0 ]; then
    # Keep the empty category present in git and on disk.
    : > "$here/main/.gitkeep"
    echo "note: empty manifest; no local main templates imported"
else
    # Apply local modifications after copying pristine upstream templates.
    for p in "$here"/patches/*.patch; do
        [ -e "$p" ] || continue
        patch -s -p1 -d "$here" < "$p"
    done

    # Subpackage directories in cports are symlinks to their parent template.
    # Recreate them for everything we imported.
    if git -C "$here" rev-parse --is-inside-work-tree >/dev/null 2>&1; then
        "$here/cbuild" relink-subpkgs
    else
        echo "note: not a git repository; run ./cbuild relink-subpkgs after git init"
    fi
fi

echo "done"
