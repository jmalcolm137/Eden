#!/bin/sh
# Sync the cbuild engine, architecture profiles, and repository definitions
# from an existing cports checkout.
#
# The local templates in core/, oasis/, pkgsrc/, and extra/ are never touched. This only writes
# inside this tree; the upstream checkout is read-only.
#
# Usage:
#   tools/sync-engine.sh [/path/to/cports]
#
# The default upstream path is ../cports relative to this tree.

set -eu

here=$(CDPATH= cd -- "$(dirname -- "$0")/.." && pwd)
upstream=${1:-"$here/../cports"}

if [ ! -x "$upstream/cbuild" ] || [ ! -d "$upstream/src" ]; then
    echo "error: '$upstream' does not look like a cports checkout" >&2
    exit 1
fi

echo "syncing cbuild engine from $upstream"

install -m 0755 "$upstream/cbuild" "$here/cbuild"

rm -rf "$here/src"
cp -a "$upstream/src" "$here/src"
find "$here/src" -type d -name __pycache__ -prune -exec rm -rf {} +

# Local engine patches (currently: use gmake explicitly).
for p in "$here"/patches/*.patch; do
    [ -e "$p" ] || continue
    patch -s -p1 -d "$here" < "$p"
done

mkdir -p "$here/etc"
rm -rf "$here/etc/build_profiles"
cp -a "$upstream/etc/build_profiles" "$here/etc/build_profiles"
# The local tree uses only the Eden repositories.
sed -i 's/\(repos[[:space:]]*=[[:space:]]*main\)[[:space:]]\+user/\1/' "$here"/etc/build_profiles/*.ini
sed -i 's|^\(repos[[:space:]]*=\).*|\1 core oasis pkgsrc extra|' "$here/etc/build_profiles/x86_64.ini"
cp -a "$upstream/etc/config.ini.example" "$here/etc/config.ini.example"
sed -i 's|repo = https://repo.chimera-linux.org/current|repo = https://repos.eden-linux.org|' "$here/etc/config.ini.example"

# Repository definitions; keep the Eden mirror and trust only our key.
rm -rf "$here/etc/apk"
cp -a "$upstream/etc/apk" "$here/etc/apk"
rm -f "$here"/etc/apk/keys/*@chimera-linux.org*.pub
cat > "$here/etc/apk/repositories.d/01-repos-remote.conf" <<'EOF'
@mirror@/@section@
@mirror@/@section@/debug
EOF

for f in COPYING.md .flake8 pyproject.toml; do
    if [ -f "$upstream/$f" ]; then
        cp -a "$upstream/$f" "$here/$f"
    fi
done

echo "done; local templates were left alone"
