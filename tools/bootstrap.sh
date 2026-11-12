#!/bin/sh
# Generate a signing key if needed, then assemble bldroot/ from Chimera
# binary packages. This is the fast bootstrap path.
#
# Extra arguments are passed to `cbuild bootstrap`, e.g.:
#   tools/bootstrap.sh -b bldroot-test

set -eu

here=$(CDPATH= cd -- "$(dirname -- "$0")/.." && pwd)
cd "$here"

key=$(sed -n 's/^[[:space:]]*key[[:space:]]*=[[:space:]]*//p' etc/config.ini | head -n 1)

if [ -z "$key" ]; then
    echo "error: no signing key configured in etc/config.ini" >&2
    exit 1
fi

if [ ! -f "etc/keys/$key" ]; then
    echo "no key at etc/keys/$key; generating one"
    ./cbuild keygen
fi

exec ./cbuild bootstrap "$@"
