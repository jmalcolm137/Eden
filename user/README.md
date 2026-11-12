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
on purpose: the tree only carries the minimal bootstrap closure in `main/`.
