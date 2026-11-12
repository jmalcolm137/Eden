#!/bin/sh
# Verify that this tree is internally complete for a source bootstrap.
#
# Checks:
#   1. every manifest entry exists and has a template.py
#   2. every non-comment manifest entry is unique
#   3. the graph cbuild computes locally matches the manifest exactly
#
# Run from anywhere; all paths are resolved relative to this script.

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

if ! uniq -d "$tmp/manifest" | grep -q .; then
    :
else
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

if ! ./cbuild print-build-graph main/base-cbuild \
        | sed 's/^ *//' \
        | sort -u > "$tmp/graph"; then
    echo "error: cbuild failed to produce the build graph" >&2
    fail=1
fi

if ! diff -u "$tmp/manifest" "$tmp/graph"; then
    echo "error: local build graph does not match the manifest" >&2
    fail=1
fi

if [ "$fail" -ne 0 ]; then
    exit 1
fi

echo "ok: $(wc -l < "$tmp/manifest") templates; graph matches manifest"
