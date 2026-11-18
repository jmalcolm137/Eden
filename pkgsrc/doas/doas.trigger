#!/bin/sh

for f in "$@"; do
    [ "$f" = "/usr/bin/doas" ] || continue
    chown root:root "$f" 2>/dev/null || :
    chmod 4755 "$f" 2>/dev/null || :
done
