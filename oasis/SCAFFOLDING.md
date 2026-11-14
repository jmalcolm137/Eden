# Scaffolded Oasis packages

No packages remain scaffolded-only: every Oasis `pkg/` entry now has a
`template.py` in this repository.

5 templates are intentionally marked broken because their
build dependencies or source acquisition are not yet available:

| Package | Blocker |
| --- | --- |
| `acme-client` | blocked on the Oasis openbsd source/header package |
| `libfido2` | requires the Oasis openbsd libbsd/header package |
| `mpv` | requires a full libplacebo build not yet available in the tree |
| `openbsd` | large OpenBSD source package not yet ported |
| `zfs` | kernel/userland ZFS build not yet ported |
