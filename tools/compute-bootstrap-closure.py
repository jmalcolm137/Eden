#!/usr/bin/env python3
"""Compute the source-template closure actually needed by source-bootstrap.

This uses the cbuild engine in this tree but reads templates from an upstream
cports checkout (read-only), so it does not require a populated main/ here.

Usage:
    tools/compute-bootstrap-closure.py [/path/to/cports] [stage ...]

Default upstream: ../cports
Default stages:   0 1   (stage 1 and 2 have the same dependency set)

Output: one source template directory name per line, sorted.
"""

import configparser
import os
import pathlib
import sys

sys.dont_write_bytecode = True

here = pathlib.Path(__file__).resolve().parent.parent
upstream = pathlib.Path(sys.argv[1] if len(sys.argv) > 1 else here / ".." / "cports")
stages = [int(x) for x in sys.argv[2:]] or [0, 1]

sys.path.insert(0, str(here / "src"))
os.chdir(here)

from cbuild.core import chroot, paths, profile, spdx, template  # noqa: E402

paths.init(
    str(here / "src"),
    str(upstream),
    "bldroot",
    "",
    "packages",
    None,
    "pkgstage",
    "sources",
    "cbuild_cache",
)
profile.init(configparser.ConfigParser())
chroot.set_host("x86_64")
spdx.init()
template.register_cats(["main", "user"])

cache = {}


def read_tmpl(pn, stage):
    key = (pn, stage)
    if key not in cache:
        cache[key] = template.Template(
            pn,
            "x86_64",
            False,
            False,
            (1, 1),
            False,
            False,
            None,
            target="lint",
            stage=stage,
        )
    return cache[key]


seen = {}


def walk(pn, stage):
    key = (pn, stage)
    if key in seen:
        return
    seen[key] = True

    try:
        tmpl = read_tmpl(pn, stage)
    except Exception as exc:  # noqa: BLE001
        print(f"warning: {pn} (stage {stage}): {exc}", file=sys.stderr)
        return

    for dep in tmpl.get_build_deps():
        walk(dep, stage)


for st in stages:
    walk("main/base-cbuild", st)

templates = sorted({pn.split("/", 1)[1] for pn, _ in seen})
for pn in templates:
    print(pn)

print(f"# {len(templates)} templates for stages {stages}", file=sys.stderr)
