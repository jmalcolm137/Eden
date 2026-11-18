# pkgsrc repository

Packages ported from pkgsrc that do not belong in core or oasis.

These packages follow pkgsrc's normal build conventions: they are **not**
required to be static-pie. Static-pie is an OASIS policy for the `core` and
`oasis` userland; pkgsrc ports may link dynamically (for example, `nodejs`).
