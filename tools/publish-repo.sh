#!/bin/sh
# Publish the built apk package repositories to Cloudflare R2.
#
# The bucket is laid out exactly as the public mirror:
#
#   core/x86_64/...              core/debug/x86_64/...
#   oasis/x86_64/...             oasis/debug/x86_64/...
#   pkgsrc/x86_64/...            pkgsrc/debug/x86_64/...
#   extra/x86_64/...             extra/debug/x86_64/...
#   keys/oasis-local.rsa.pub
#
# Packages are uploaded before indexes, and stale packages are removed first
# (only with --prune), so a published index only ever points at packages that
# are already on the bucket.
#
# Examples:
#   tools/publish-repo.sh --dry-run
#   tools/publish-repo.sh
#   tools/publish-repo.sh --prune --verify
#   tools/publish-repo.sh --refresh          # re-upload to update object headers
#   tools/publish-repo.sh --no-debug core oasis
#
# Environment overrides:
#   EDEN_REPO_SRC   built repository root          (default: scratch-repo)
#   R2_REMOTE       rclone remote name             (default: halcyon)
#   R2_BUCKET       bucket name                    (default: eden-repos)
#   R2_DEST         full rclone destination        (default: $R2_REMOTE:$R2_BUCKET)
#   EDEN_ARCH       architecture directory         (default: x86_64)
#   PUBLIC_BASE     public mirror URL              (default: https://repos.eden-linux.org)
#   REPO_KEY        public signing key to publish  (default: etc/keys/oasis-local.rsa.pub)

set -eu

src=${EDEN_REPO_SRC:-scratch-repo}
remote=${R2_REMOTE:-halcyon}
bucket=${R2_BUCKET:-eden-repos}
arch=${EDEN_ARCH:-x86_64}
public_base=${PUBLIC_BASE:-https://repos.eden-linux.org}
key_file=${REPO_KEY:-etc/keys/oasis-local.rsa.pub}

repos="core oasis pkgsrc extra"
debug=1
prune=0
verify=0
dry_run=0
refresh=0

usage() {
    sed -n '2,30p' "$0" | sed 's/^# \{0,1\}//'
}

die() {
    echo "error: $*" >&2
    exit 1
}

while [ $# -gt 0 ]; do
    case $1 in
        -n|--dry-run) dry_run=1 ;;
        --prune) prune=1 ;;
        --verify) verify=1 ;;
        --no-debug) debug=0 ;;
        --refresh) refresh=1 ;;
        --src)
            [ $# -ge 2 ] || die "--src needs a value"
            src=$2
            shift
            ;;
        --arch)
            [ $# -ge 2 ] || die "--arch needs a value"
            arch=$2
            shift
            ;;
        --remote)
            [ $# -ge 2 ] || die "--remote needs a value"
            remote=$2
            shift
            ;;
        --bucket)
            [ $# -ge 2 ] || die "--bucket needs a value"
            bucket=$2
            shift
            ;;
        --public-base)
            [ $# -ge 2 ] || die "--public-base needs a value"
            public_base=$2
            shift
            ;;
        -h|--help)
            usage
            exit 0
            ;;
        -*)
            usage >&2
            die "unknown option: $1"
            ;;
        *)
            repos="$*"
            break
            ;;
    esac
    shift
done

command -v rclone >/dev/null 2>&1 || die "rclone is not installed"
command -v curl >/dev/null 2>&1 || die "curl is not installed"
[ -d "$src" ] || die "repository root not found: $src"

dest=${R2_DEST:-"$remote:$bucket"}
dry=
[ "$dry_run" = 1 ] && dry=--dry-run
refresh_flag=
[ "$refresh" = 1 ] && refresh_flag=--ignore-times

# Bucket-scoped R2 tokens cannot create or list buckets, so never let rclone
# try to create the destination. Local test destinations (no colon) skip it.
s3flags=
case "$dest" in
    *:*) s3flags=--s3-no-check-bucket ;;
esac

tmpdir=$(mktemp -d)
trap 'rm -rf "$tmpdir"' EXIT INT TERM

# Fail early with a useful message instead of a raw S3 error. Bucket-scoped
# tokens can list inside their bucket, so this also validates the credentials.
if [ "$dry_run" != 1 ]; then
    case "$dest" in
        *:*)
            if ! rclone lsf "$dest" --max-depth 1 $s3flags >/dev/null 2>&1; then
                die "cannot access $dest; create the bucket and check docs/r2-repos.md"
            fi
            ;;
    esac
fi

rclone_common="--transfers 8 --checkers 8 --stats-one-line --stats 15s"

copy_packages() {
    echo "==> packages $1 -> $2"
    # shellcheck disable=SC2086
    rclone copy "$1" "$2" \
        --include '*.apk' \
        --header-upload 'Cache-Control: public, max-age=31536000, immutable' \
        --header-upload 'Content-Type: application/octet-stream' $refresh_flag \
        $rclone_common $dry $s3flags
}

copy_index() {
    echo "==> index    $1 -> $2"
    # shellcheck disable=SC2086
    rclone copy "$1" "$2" \
        --include 'Packages.adb' \
        --include 'APKINDEX.tar.gz' \
        --header-upload 'Cache-Control: no-cache, max-age=0, must-revalidate' \
        --header-upload 'Content-Type: application/octet-stream' $refresh_flag \
        $rclone_common $dry $s3flags
}

prune_packages() {
    localf=$tmpdir/local
    remotef=$tmpdir/remote
    stale=$tmpdir/stale

    find "$1" -maxdepth 1 -type f -name '*.apk' -exec basename {} \; | sort > "$localf"

    # shellcheck disable=SC2086
    if ! rclone lsf "$2" --files-only --max-depth 1 $s3flags > "$remotef" 2>/dev/null; then
        echo "    remote listing unavailable; skipping prune of $2" >&2
        return 0
    fi

    grep -E '\.apk$' "$remotef" | sort > "$remotef.apk" || true
    comm -13 "$localf" "$remotef.apk" > "$stale"
    count=$(wc -l < "$stale" | tr -d ' ')

    if [ "$count" -eq 0 ]; then
        echo "    no stale packages in $2"
        return 0
    fi

    echo "    pruning $count stale package(s) from $2"
    if [ "$dry_run" = 1 ]; then
        sed 's/^/      /' "$stale"
        return 0
    fi

    # shellcheck disable=SC2086
    rclone delete "$2" --files-from-raw "$stale" $s3flags
}

publish_repo() {
    repo=$1
    base=$src/$repo/$arch
    dbg=

    [ -d "$base" ] || die "missing architecture directory: $base"
    [ -f "$base/Packages.adb" ] || die "missing index: $base/Packages.adb"

    if [ "$debug" = 1 ] && [ -d "$src/$repo/debug/$arch" ]; then
        if [ -f "$src/$repo/debug/$arch/Packages.adb" ]; then
            dbg=$src/$repo/debug/$arch
        else
            echo "warning: $src/$repo/debug/$arch has no index; skipping debug packages" >&2
        fi
    fi

    if [ "$prune" = 1 ]; then
        prune_packages "$base" "$dest/$repo/$arch"
        [ -z "$dbg" ] || prune_packages "$dbg" "$dest/$repo/debug/$arch"
    fi

    copy_packages "$base" "$dest/$repo/$arch"
    [ -z "$dbg" ] || copy_packages "$dbg" "$dest/$repo/debug/$arch"

    # Indexes last: clients must never see an index that references a package
    # which has not reached the bucket yet.
    [ -z "$dbg" ] || copy_index "$dbg" "$dest/$repo/debug/$arch"
    copy_index "$base" "$dest/$repo/$arch"
}

verify_repo() {
    repo=$1
    base=$src/$repo/$arch
    url=$public_base/$repo/$arch/Packages.adb
    printf '    %-52s ' "$url"

    if ! head=$(curl -fsSI --max-time 30 "$url" 2>/dev/null); then
        echo FAILED
        return 1
    fi

    cc=$(printf '%s\n' "$head" | tr -d '\r' |
        awk -F': ' 'tolower($1) == "cache-control" { print $2; exit }')
    echo "ok${cc:+ (cache-control: $cc)}"

    # Also check one package, so missing cache metadata is caught.
    set -- "$base"/*.apk
    [ -f "$1" ] || return 0
    pkg=$(basename "$1")
    purl=$public_base/$repo/$arch/$pkg
    printf '    %-52s ' "$purl"

    if ! head=$(curl -fsSI --max-time 30 "$purl" 2>/dev/null); then
        echo FAILED
        return 1
    fi

    cc=$(printf '%s\n' "$head" | tr -d '\r' |
        awk -F': ' 'tolower($1) == "cache-control" { print $2; exit }')
    case "$cc" in
        *immutable*) echo "ok (cache-control: $cc)" ;;
        *) echo "ok, but cache-control is missing 'immutable'${cc:+ ($cc)}"; return 1 ;;
    esac
}

for repo in $repos; do
    echo "==> repo $repo ($arch)"
    publish_repo "$repo"
done

if [ -f "$key_file" ]; then
    echo "==> key    $key_file -> $dest/keys"
    # shellcheck disable=SC2086
    rclone copyto "$key_file" "$dest/keys/$(basename "$key_file")" \
        --header-upload 'Cache-Control: public, max-age=86400' \
        $rclone_common $dry $s3flags $refresh_flag
else
    echo "warning: public key not found: $key_file" >&2
fi

if [ "$dry_run" != 1 ] && [ "$verify" = 1 ]; then
    echo "==> verify $public_base"
    failed=0
    for repo in $repos; do
        verify_repo "$repo" || failed=1
    done
    [ "$failed" = 0 ] || die "mirror verification failed"
fi

if [ "$dry_run" != 1 ]; then
    echo
    echo "Published to $dest."
    echo "Clients can use:"
    for repo in $repos; do
        echo "  $public_base/$repo"
    done
    echo
    echo "Key: $public_base/keys/$(basename "$key_file")"
fi
