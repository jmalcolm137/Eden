#!/bin/sh
# Build the Oasis-composed cbuild environment.
#
# 1. Create a temporary Chimera binary bldroot. It provides gzip and the
#    toolchain needed to build the local packages.
# 2. Build the local Oasis packages and the custom base-cbuild meta using
#    that temporary root.
# 3. Create bldroot-oasis from the local base-cbuild. The result contains
#    Chimera clang/llvm/lld, gmake, musl, apk-tools and bsdtar, plus Oasis
#    sbase/ubase/oksh/pigz userland, without chimerautils.
#
# Use -b bldroot-oasis (or move it to bldroot) afterwards.

set -eu

here=$(CDPATH= cd -- "$(dirname -- "$0")/.." && pwd)
cd "$here"

key=$(sed -n 's/^[[:space:]]*key[[:space:]]*=[[:space:]]*//p' etc/config.ini | head -n 1)
if [ -z "$key" ]; then
    echo "error: no signing key configured in etc/config.ini" >&2
    exit 1
fi
if [ ! -f "etc/keys/$key" ]; then
    ./cbuild keygen
fi

tmp_repo=.bootstrap-repo
tmp_root=bldroot-chimera

if [ ! -f "$tmp_root/.cbuild_chroot_init" ]; then
    echo "==> creating temporary Chimera bldroot"
    rm -rf "$tmp_repo"
    mkdir -p "$tmp_repo"
    ./cbuild -r "$tmp_repo" -b "$tmp_root" bootstrap
fi

# Build into a separate repo so the temporary root stays a Chimera root
# (with chimerautils' grep/awk/gzip) until every package has been built.
# gmake is first: once base-cbuild is built it pulls in the Oasis userland,
# which intentionally does not provide everything autoconf expects.
for p in \
    byacc \
    awk \
    sed \
    diffutils \
    patch \
    pkgconf \
    gmake \
    m4 \
    flex \
    base-files \
    linux-personality \
    oksh \
    pigz \
    sbase \
    ubase \
    ca-certificates \
    zlib-static \
    xz \
    bzip2 \
    lz4 \
    zstd \
    acl \
    libffi8 \
    netbsd-curses \
    libedit \
    fortify-headers \
    libatomic-chimera \
    fakeroot \
    libarchive \
    bearssl \
    musl \
    perl \
    linux-headers \
    libressl \
    bubblewrap \
    curl \
    git \
    python \
    samurai \
    muon \
    cmake \
    llvm-bootstrap \
    llvm \
    apk-tools \
    base-cbuild
do
    echo "==> building core/$p"
    ./cbuild -r "$tmp_repo" -b "$tmp_root" -f pkg "core/$p"
done

echo "==> creating bldroot-oasis from the local base-cbuild"
if [ -e bldroot-oasis ]; then
    ./cbuild -b bldroot-oasis zap
fi
./cbuild -r "$tmp_repo" -b bldroot-oasis bootstrap

echo
echo "done: bldroot-oasis is the Oasis-composed build root"
echo "build packages with: ./cbuild -b bldroot-oasis pkg oasis/<name>"
