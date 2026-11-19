#!/bin/sh
# offline bison: serve the pregenerated parsers shipped with the package
out=
def=
input=
while [ $# -gt 0 ]; do
    case "$1" in
        -o) out="$2"; shift 2 ;;
        --defines=*) def="${1#--defines=}"; shift ;;
        -*) shift ;;
        *) input="$1"; shift ;;
    esac
done
[ -n "$out" ] || exit 1
base=$(basename "$input" .y)
src="$PWD/.bison-pregen/$base.tab.c"
hdr="$PWD/.bison-pregen/$base.tab.h"
[ -f "$src" ] || exit 1
cp "$src" "$out" || exit 1
[ -n "$def" ] && cp "$hdr" "$def"
exit 0
