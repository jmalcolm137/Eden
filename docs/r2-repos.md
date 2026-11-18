# Publishing the repositories to Cloudflare R2

The built repositories are published to the `eden-repos` R2 bucket and served
at **https://repos.eden-linux.org**:

```
https://repos.eden-linux.org/
├── keys/oasis-local.rsa.pub
├── distfiles/
│   ├── cargo-1.98.0-x86_64-chimera-linux-musl.tar.xz
│   ├── rust-std-1.98.0-x86_64-chimera-linux-musl.tar.xz
│   └── rustc-1.98.0-x86_64-chimera-linux-musl.tar.xz
├── core/x86_64/...
├── core/debug/x86_64/...
├── oasis/x86_64/...
├── oasis/debug/x86_64/...
├── pkgsrc/x86_64/...
├── pkgsrc/debug/x86_64/...
├── extra/x86_64/...
└── extra/debug/x86_64/...
```

The `distfiles/` objects are the Rust stage-0 tarballs used by
`pkgsrc/rust-bootstrap` and `pkgsrc/cargo-bootstrap`, so those packages no
longer download from a Chimera host.

The object layout is exactly the local one, so an apk repository URL is
`https://repos.eden-linux.org/<repo>` and apk appends `/<arch>` itself.

## One-time Cloudflare setup

The Cloudflare account needs the `eden-linux.org` zone, and the bucket must be
in the same account as that zone. The R2 API token used by rclone is
bucket-scoped (Object Read & Write), so it cannot create buckets or list them;
create the bucket with the dashboard or a separate admin token first.

### 1. Create the bucket

1. Open **R2 object storage → Overview** in the Cloudflare dashboard.
2. Select **Create bucket**.
3. Name it `eden-repos`; leave the location and storage class at their
   defaults.
4. Create the bucket. Do **not** enable the `r2.dev` public URL; the custom
   domain below is the production access path.

### 2. Create the S3 credentials

1. On the **R2 → Overview** page, under **Account Details**, select **Manage**
   next to **API Tokens**.
2. Create a token with **Object Read & Write** permission, scoped to the
   `eden-repos` bucket.
3. Record the **Access Key ID** and **Secret Access Key** (the secret is shown
   only once), and note the S3 endpoint:
   `https://<ACCOUNT_ID>.r2.cloudflarestorage.com`.

Configure rclone (interactive so the secret is not left in shell history):

```
rclone config create halcyon s3 provider=Cloudflare region=auto \
    endpoint=https://<ACCOUNT_ID>.r2.cloudflarestorage.com \
    access_key_id=<ACCESS_KEY_ID> secret_access_key=<SECRET>
```

The existing `halcyon` remote already uses this shape; update its key and
endpoint if the account or token changes. The credentials live in
`~/.config/rclone/rclone.conf` (`0600`); keep that file out of git.

### 3. Attach the custom domain

1. **R2 → eden-repos → Settings → Custom Domains → Add**.
2. Enter `repos.eden-linux.org` and continue.
3. Review the DNS record Cloudflare will add (a proxied CNAME in the
   `eden-linux.org` zone) and select **Connect Domain**.

The status changes from **Initializing** to **Active** within a few minutes.
If it stays initializing, use **Retry connection** from the bucket's `...`
menu. The zone must be active on Cloudflare; on Enterprise plans release any
zone hold first.

### 4. Cache rules

Cloudflare does not cache `.apk` by default, and it caches `.gz` by default, so
create two cache rules under **Caching → Cache Rules** for
`http.host eq "repos.eden-linux.org"`:

| Order | Match | Action |
|---|---|---|
| 1 | URI path ends with `/Packages.adb` **or** `/APKINDEX.tar.gz` | **Bypass cache** |
| 2 | URI path ends with `.apk` | **Eligible for cache**, Edge TTL *Use cache-control header if present*, Browser TTL *Respect origin* |

The publish script already sets `Cache-Control: no-cache` on indexes and
`public, max-age=31536000, immutable` on packages, so the rules above make the
headers effective without ever serving a stale index.

Optional but recommended: enable **Smart Tiered Cache** for the zone to keep
one upper-tier cache near the bucket.

## Publishing

Build packages into the usual repository path (for example `scratch-repo`),
then:

```
tools/publish-repo.sh --dry-run          # show what would change
tools/publish-repo.sh                    # upload packages, then indexes, then key
tools/publish-repo.sh --prune --verify   # remove old versions and check the mirror
tools/publish-repo.sh --refresh          # re-upload even if size/time match
```

The script:

- uploads `*.apk` first and `Packages.adb`/`APKINDEX.tar.gz` last, so an index
  never points at a package that is not yet on the bucket;
- optionally removes packages that are no longer in the local repository
  (`--prune`), before uploading anything;
- publishes `etc/keys/oasis-local.rsa.pub` as `/keys/oasis-local.rsa.pub`;
- sets long-lived immutable caching on packages and `no-cache` on indexes;
- with `--verify`, checks every published index and one package per repository
  over HTTPS, including their `Cache-Control` headers.

`--refresh` forces re-upload of objects that rclone would otherwise skip. Use
it once after changing the cache policy, or when objects were uploaded by other
means and are missing the cache headers.

The first upload is about 1.2 GB for all four repos including debug packages.
Useful overrides:

```
tools/publish-repo.sh --src scratch-repo --arch x86_64
tools/publish-repo.sh --bucket other-bucket
tools/publish-repo.sh --no-debug core oasis
R2_DEST=/tmp/eden-mirror tools/publish-repo.sh --prune core   # local test
```

Repositories are listed explicitly by default (`core oasis pkgsrc extra`); to
publish only some, pass them as arguments.

## Client setup

Install the repository key first:

```
doas mkdir -p /etc/apk/keys
doas curl -fsSL -o /etc/apk/keys/oasis-local.rsa.pub \
    https://repos.eden-linux.org/keys/oasis-local.rsa.pub
```

Then add the repositories (debug packages are optional):

```
# /etc/apk/repositories
https://repos.eden-linux.org/core
https://repos.eden-linux.org/oasis
https://repos.eden-linux.org/pkgsrc
https://repos.eden-linux.org/extra

# debug symbols
https://repos.eden-linux.org/core/debug
https://repos.eden-linux.org/oasis/debug
https://repos.eden-linux.org/pkgsrc/debug
https://repos.eden-linux.org/extra/debug
```

```
apk update
apk add <package>
```

Only the apk v3 (`Packages.adb`/ADB) index format is published, matching the
apk-tools in `core/`.

### Using the mirror from cbuild

The tree is already configured to use the published mirror:

```
# etc/config.ini
[apk]
repo = https://repos.eden-linux.org
```

`etc/apk/repositories.d/01-repos-remote.conf` holds the remote repository
templates, and `etc/build_profiles/x86_64.ini` lists
`repos = core oasis pkgsrc extra`. `@mirror@` is substituted with the
`[apk] repo` value, so `./cbuild bootstrap` installs the stage-0 bldroot
directly from `https://repos.eden-linux.org` and never consults Chimera.

The only external binary inputs are the published Eden packages used for that
stage-0 root and the official Rust stage0 tarballs; everything else is rebuilt
from the templates in this tree.

## Verification and maintenance

```
curl -fsSI https://repos.eden-linux.org/core/x86_64/Packages.adb
curl -fsSI https://repos.eden-linux.org/core/x86_64/acl-2.4.0-r1.apk
curl -fsS  https://repos.eden-linux.org/keys/oasis-local.rsa.pub
```

Expected headers: indexes `cache-control: no-cache, max-age=0,
must-revalidate`; packages `cache-control: public, max-age=31536000,
immutable`.

If a key is rotated, publish the new public key and purge the old object from
the Cloudflare cache (**Caching → Configuration → Purge cache → By URL** for
`https://repos.eden-linux.org/keys/oasis-local.rsa.pub`). Changing a signing
key requires clients to install the new public key before upgrading; the old
packages remain signed by the old key.
