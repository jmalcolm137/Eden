# user category

Put local package templates here, one directory per package:

```
user/<pkgname>/template.py
user/<pkgname>/files/...
user/<pkgname>/patches/...
```

Then build with:

```
./cbuild pkg user/<pkgname>
```

See the upstream `Packaging.md` for the template API. This category is empty
on purpose: `main/` only carries the 66 templates needed for
`./cbuild source-bootstrap`.
