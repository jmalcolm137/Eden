/* crypto_bearssl.c - BearSSL crypto backend for apk-tools
 *
 * SPDX-License-Identifier: GPL-2.0-only
 */

#include <errno.h>
#include <fcntl.h>
#include <stdlib.h>
#include <string.h>
#include <sys/stat.h>
#include <unistd.h>

#include <bearssl.h>

#include "apk_crypto.h"

struct apk_bearssl_digest {
	uint8_t alg;
	struct apk_pkey *pkey;
	union {
		br_sha1_context sha1;
		br_sha256_context sha256;
		br_sha512_context sha512;
	} u;
};

struct apk_bearssl_pkey {
	int is_priv;
	br_skey_decoder_context sk;
	br_rsa_public_key pub;
	unsigned char *pubder;
	size_t pubder_len;
};

struct der_cursor {
	const unsigned char *p;
	size_t len;
};

static int der_next(struct der_cursor *c, unsigned char *tag,
	const unsigned char **val, size_t *vlen,
	const unsigned char **start, size_t *tlvlen)
{
	const unsigned char *p = c->p, *s = p;
	size_t len, n;

	if (c->len < 2) return -1;
	*tag = *p++;
	len = *p++;
	if (len & 0x80) {
		n = len & 0x7f;
		if (n == 0 || n > sizeof(size_t) || c->len < n + 2) return -1;
		len = 0;
		while (n-- > 0) len = (len << 8) | *p++;
	}
	if (c->len < (size_t)(p - c->p) + len) return -1;
	*val = p;
	*vlen = len;
	if (start) *start = s;
	if (tlvlen) *tlvlen = (size_t)(p - s) + len;
	c->p = p + len;
	c->len -= (size_t)(p - s) + len;
	return 0;
}

static int der_enter(const unsigned char *val, size_t len, struct der_cursor *c)
{
	c->p = val;
	c->len = len;
	return 0;
}

static int parse_rsa_priv(const unsigned char *der, size_t derlen,
	const unsigned char **n, size_t *nlen,
	const unsigned char **e, size_t *elen)
{
	struct der_cursor outer, seq;
	unsigned char tag;
	const unsigned char *v;
	size_t vl;

	if (der_next(&(struct der_cursor){ der, derlen }, &tag, &v, &vl,
		NULL, NULL) < 0 || tag != 0x30) return -1;
	der_enter(v, vl, &seq);
	/* version */
	if (der_next(&seq, &tag, &v, &vl, NULL, NULL) < 0 || tag != 0x02)
		return -1;
	/* n */
	if (der_next(&seq, &tag, n, nlen, NULL, NULL) < 0 || tag != 0x02)
		return -1;
	/* e */
	if (der_next(&seq, &tag, e, elen, NULL, NULL) < 0 || tag != 0x02)
		return -1;
	(void)outer;
	return 0;
}

static int parse_rsa_priv_any(const unsigned char *der, size_t derlen,
	const unsigned char **n, size_t *nlen,
	const unsigned char **e, size_t *elen)
{
	struct der_cursor c;
	unsigned char tag;
	const unsigned char *v, *v2;
	size_t vl, vl2;

	if (der_next(&(struct der_cursor){ der, derlen }, &tag, &v, &vl,
		NULL, NULL) < 0 || tag != 0x30) return -1;
	der_enter(v, vl, &c);
	if (der_next(&c, &tag, &v2, &vl2, NULL, NULL) < 0 || tag != 0x02)
		return -1;
	/* Peek at the next element: PKCS#8 has an AlgorithmIdentifier
	 * SEQUENCE after the version INTEGER. */
	if (vl2 == 1 && v2[0] == 0 && c.len >= 2 && c.p[0] == 0x30) {
		/* skip AlgorithmIdentifier */
		if (der_next(&c, &tag, &v, &vl, NULL, NULL) < 0 || tag != 0x30)
			return -1;
		/* OCTET STRING containing PKCS#1 RSAPrivateKey */
		if (der_next(&c, &tag, &v, &vl, NULL, NULL) < 0 || tag != 0x04)
			return -1;
		return parse_rsa_priv(v, vl, n, nlen, e, elen);
	}
	/* Plain PKCS#1 */
	return parse_rsa_priv(der, derlen, n, nlen, e, elen);
}

static int parse_rsa_pub(const unsigned char *der, size_t derlen,
	const unsigned char **n, size_t *nlen,
	const unsigned char **e, size_t *elen,
	const unsigned char **pubder, size_t *pubderlen)
{
	struct der_cursor outer, c;
	unsigned char tag;
	const unsigned char *v, *v2, *s;
	size_t vl, vl2, sl;

	if (der_next(&(struct der_cursor){ der, derlen }, &tag, &v, &vl,
		&s, &sl) < 0 || tag != 0x30) return -1;
	der_enter(v, vl, &outer);
	if (der_next(&outer, &tag, &v, &vl, NULL, NULL) < 0) return -1;
	if (tag == 0x02) {
		/* PKCS#1 RSAPublicKey: n, e */
		*pubder = s;
		*pubderlen = sl;
		*n = v;
		*nlen = vl;
		if (der_next(&outer, &tag, e, elen, NULL, NULL) < 0 ||
			tag != 0x02) return -1;
		return 0;
	}
	if (tag != 0x30) return -1;
	/* SubjectPublicKeyInfo: alg, bit string */
	if (der_next(&outer, &tag, &v2, &vl2, &s, &sl) < 0 || tag != 0x03)
		return -1;
	if (vl2 < 2 || v2[0] != 0) return -1;
	der_enter(v2 + 1, vl2 - 1, &c);
	if (der_next(&c, &tag, &v, &vl, &s, &sl) < 0 || tag != 0x30)
		return -1;
	der_enter(v, vl, &c);
	if (der_next(&c, &tag, n, nlen, NULL, NULL) < 0 || tag != 0x02)
		return -1;
	if (der_next(&c, &tag, e, elen, NULL, NULL) < 0 || tag != 0x02)
		return -1;
	*pubder = s;
	*pubderlen = sl;
	(void)pubderlen;
	return 0;
}

static unsigned char *put_der_len(unsigned char *p, size_t len)
{
	if (len < 0x80) {
		*p++ = len;
	} else {
		unsigned char tmp[sizeof(size_t)];
		size_t n = 0;
		while (len) { tmp[n++] = len & 0xff; len >>= 8; }
		*p++ = 0x80 | n;
		while (n) *p++ = tmp[--n];
	}
	return p;
}

static size_t der_len_bytes(size_t len)
{
	size_t n = 1;
	if (len < 0x80) return 1;
	while (len) { n++; len >>= 8; }
	return n;
}

static size_t tlv_len(size_t len)
{
	return 1 + der_len_bytes(len) + len;
}

static unsigned char *encode_rsa_pub(const unsigned char *n, size_t nlen,
	const unsigned char *e, size_t elen, size_t *outlen)
{
	size_t ilen = tlv_len(nlen) + tlv_len(elen);
	size_t total = tlv_len(ilen);
	unsigned char *out = malloc(total), *p;

	if (!out) return NULL;
	p = out;
	*p++ = 0x30;
	p = put_der_len(p, ilen);
	*p++ = 0x02;
	p = put_der_len(p, nlen);
	memcpy(p, n, nlen); p += nlen;
	*p++ = 0x02;
	p = put_der_len(p, elen);
	memcpy(p, e, elen); p += elen;
	*outlen = (size_t)(p - out);
	return out;
}

static void sha512_id(const unsigned char *der, size_t len, unsigned char id[16])
{
	br_sha512_context c;
	unsigned char out[64];

	br_sha512_init(&c);
	br_sha512_update(&c, der, len);
	br_sha512_out(&c, out);
	memcpy(id, out, 16);
}

static const unsigned char *alg_oid(uint8_t alg)
{
	switch (alg) {
	case APK_DIGEST_SHA1: return BR_HASH_OID_SHA1;
	case APK_DIGEST_SHA256:
	case APK_DIGEST_SHA256_160: return BR_HASH_OID_SHA256;
	case APK_DIGEST_SHA512: return BR_HASH_OID_SHA512;
	default: return NULL;
	}
}

static size_t alg_len(uint8_t alg)
{
	switch (alg) {
	case APK_DIGEST_SHA1: return 20;
	case APK_DIGEST_SHA256:
	case APK_DIGEST_SHA256_160: return 32;
	case APK_DIGEST_SHA512: return 64;
	default: return 0;
	}
}

static void digest_init(struct apk_bearssl_digest *d, uint8_t alg)
{
	d->alg = alg;
	switch (alg) {
	case APK_DIGEST_SHA1: br_sha1_init(&d->u.sha1); break;
	case APK_DIGEST_SHA256:
	case APK_DIGEST_SHA256_160: br_sha256_init(&d->u.sha256); break;
	case APK_DIGEST_SHA512: br_sha512_init(&d->u.sha512); break;
	}
}

static void digest_update(struct apk_bearssl_digest *d, const void *p, size_t len)
{
	switch (d->alg) {
	case APK_DIGEST_SHA1: br_sha1_update(&d->u.sha1, p, len); break;
	case APK_DIGEST_SHA256:
	case APK_DIGEST_SHA256_160: br_sha256_update(&d->u.sha256, p, len); break;
	case APK_DIGEST_SHA512: br_sha512_update(&d->u.sha512, p, len); break;
	}
}

static void digest_out(struct apk_bearssl_digest *d, unsigned char *out)
{
	switch (d->alg) {
	case APK_DIGEST_SHA1: br_sha1_out(&d->u.sha1, out); break;
	case APK_DIGEST_SHA256:
	case APK_DIGEST_SHA256_160: br_sha256_out(&d->u.sha256, out); break;
	case APK_DIGEST_SHA512: br_sha512_out(&d->u.sha512, out); break;
	}
}

static struct apk_bearssl_digest *bdigest(struct apk_digest_ctx *dctx)
{
	return dctx->priv;
}

static struct apk_bearssl_pkey *bkey(struct apk_pkey *pkey)
{
	return pkey->priv;
}

int apk_digest_calc(struct apk_digest *d, uint8_t alg, const void *ptr, size_t sz)
{
	struct apk_bearssl_digest tmp;

	if (!alg_len(alg)) return -APKE_CRYPTO_ERROR;
	digest_init(&tmp, alg);
	digest_update(&tmp, ptr, sz);
	digest_out(&tmp, d->data);
	d->alg = alg;
	d->len = apk_digest_alg_len(alg);
	return 0;
}

int apk_digest_ctx_init(struct apk_digest_ctx *dctx, uint8_t alg)
{
	struct apk_bearssl_digest *d = calloc(1, sizeof *d);
	if (!d) return -ENOMEM;
	dctx->alg = alg;
	dctx->priv = d;
	if (alg != APK_DIGEST_NONE) digest_init(d, alg);
	return 0;
}

int apk_digest_ctx_reset(struct apk_digest_ctx *dctx)
{
	struct apk_bearssl_digest *d = bdigest(dctx);
	if (dctx->alg != APK_DIGEST_NONE) digest_init(d, dctx->alg);
	return 0;
}

int apk_digest_ctx_reset_alg(struct apk_digest_ctx *dctx, uint8_t alg)
{
	struct apk_bearssl_digest *d = bdigest(dctx);
	if (!alg_len(alg)) return -APKE_CRYPTO_ERROR;
	dctx->alg = alg;
	digest_init(d, alg);
	return 0;
}

void apk_digest_ctx_free(struct apk_digest_ctx *dctx)
{
	free(dctx->priv);
	dctx->priv = NULL;
}

int apk_digest_ctx_update(struct apk_digest_ctx *dctx, const void *ptr, size_t sz)
{
	if (dctx->alg == APK_DIGEST_NONE) return 0;
	digest_update(bdigest(dctx), ptr, sz);
	return 0;
}

int apk_digest_ctx_final(struct apk_digest_ctx *dctx, struct apk_digest *d)
{
	struct apk_bearssl_digest *b = bdigest(dctx);
	if (dctx->alg == APK_DIGEST_NONE) {
		apk_digest_reset(d);
		return 0;
	}
	digest_out(b, d->data);
	d->alg = dctx->alg;
	d->len = apk_digest_alg_len(d->alg);
	return 0;
}

void apk_pkey_free(struct apk_pkey *pkey)
{
	struct apk_bearssl_pkey *k = bkey(pkey);
	if (k) {
		free(k->pubder);
		free(k);
	}
	pkey->priv = NULL;
}

static int read_file(int dirfd, const char *fn, unsigned char **out, size_t *outlen)
{
	struct stat st;
	unsigned char *buf;
	size_t off = 0;
	int fd;

	fd = openat(dirfd, fn, O_RDONLY | O_CLOEXEC);
	if (fd < 0) return -errno;
	if (fstat(fd, &st) < 0 || st.st_size <= 0 || st.st_size > 1048576) {
		close(fd);
		return -APKE_CRYPTO_KEY_FORMAT;
	}
	buf = malloc(st.st_size);
	if (!buf) { close(fd); return -ENOMEM; }
	while (off < (size_t)st.st_size) {
		ssize_t n = read(fd, buf + off, st.st_size - off);
		if (n <= 0) { free(buf); close(fd); return -APKE_CRYPTO_KEY_FORMAT; }
		off += n;
	}
	close(fd);
	*out = buf;
	*outlen = off;
	return 0;
}

struct pbuf { unsigned char *p; size_t len, cap; };

static void pbuf_add(void *ctx, const void *src, size_t len)
{
	struct pbuf *b = ctx;
	if (b->len + len > b->cap) {
		size_t nc = (b->len + len) * 2 + 256;
		unsigned char *np = realloc(b->p, nc);
		if (!np) return;
		b->p = np;
		b->cap = nc;
	}
	memcpy(b->p + b->len, src, len);
	b->len += len;
}

static int pem_decode(const unsigned char *in, size_t inlen, struct pbuf *out)
{
	br_pem_decoder_context pc;
	size_t off = 0;

	br_pem_decoder_init(&pc);
	br_pem_decoder_setdest(&pc, pbuf_add, out);
	while (off < inlen) {
		size_t n = br_pem_decoder_push(&pc, in + off, inlen - off);
		off += n;
		int ev = br_pem_decoder_event(&pc);
		if (ev == BR_PEM_ERROR) return -1;
		if (ev == BR_PEM_END_OBJ) return out->len > 0 ? 0 : -1;
		if (n == 0 && ev == 0) break;
	}
	return out->len > 0 ? 0 : -1;
}

static int load_priv(struct apk_bearssl_pkey *k, const unsigned char *der, size_t len,
	unsigned char id[16])
{
	const unsigned char *n, *e;
	size_t nlen, elen, publen;
	unsigned char *pub;

	br_skey_decoder_init(&k->sk);
	br_skey_decoder_push(&k->sk, der, len);
	if (br_skey_decoder_last_error(&k->sk) != 0 ||
	    br_skey_decoder_key_type(&k->sk) != BR_KEYTYPE_RSA)
		return -APKE_CRYPTO_KEY_FORMAT;
	if (parse_rsa_priv_any(der, len, &n, &nlen, &e, &elen) < 0)
		return -APKE_CRYPTO_KEY_FORMAT;
	pub = encode_rsa_pub(n, nlen, e, elen, &publen);
	if (!pub) return -ENOMEM;
	sha512_id(pub, publen, id);
	free(pub);
	k->is_priv = 1;
	return 0;
}

static int load_pub(struct apk_bearssl_pkey *k, const unsigned char *der, size_t len,
	unsigned char id[16])
{
	const unsigned char *n, *e, *pubder;
	size_t nlen, elen, publen;

	if (parse_rsa_pub(der, len, &n, &nlen, &e, &elen, &pubder, &publen) < 0)
		return -APKE_CRYPTO_KEY_FORMAT;
	k->pubder = malloc(publen);
	if (!k->pubder) return -ENOMEM;
	memcpy(k->pubder, pubder, publen);
	k->pubder_len = publen;
	k->pub.n = k->pubder + (n - pubder);
	k->pub.nlen = nlen;
	k->pub.e = k->pubder + (e - pubder);
	k->pub.elen = elen;
	sha512_id(k->pubder, k->pubder_len, id);
	k->is_priv = 0;
	return 0;
}

int apk_pkey_load(struct apk_pkey *pkey, int dirfd, const char *fn, int priv)
{
	struct apk_bearssl_pkey *k;
	struct pbuf pem = { 0 };
	unsigned char *raw = NULL, *der;
	size_t rawlen = 0, derlen;
	int r;

	r = read_file(dirfd, fn, &raw, &rawlen);
	if (r) return r;
	if (pem_decode(raw, rawlen, &pem) == 0) {
		der = pem.p;
		derlen = pem.len;
	} else {
		der = raw;
		derlen = rawlen;
	}
	k = calloc(1, sizeof *k);
	if (!k) { free(pem.p); free(raw); return -ENOMEM; }
	if (priv)
		r = load_priv(k, der, derlen, pkey->id);
	else
		r = load_pub(k, der, derlen, pkey->id);
	free(pem.p);
	free(raw);
	if (r) { free(k->pubder); free(k); return r; }
	pkey->priv = k;
	return 0;
}

int apk_sign_start(struct apk_digest_ctx *dctx, uint8_t alg, struct apk_pkey *pkey)
{
	struct apk_bearssl_digest *d = bdigest(dctx);
	struct apk_bearssl_pkey *k = bkey(pkey);
	if (!k || !k->is_priv || !alg_len(alg)) return -APKE_CRYPTO_ERROR;
	d->pkey = pkey;
	digest_init(d, alg);
	dctx->alg = alg;
	return 0;
}

int apk_sign(struct apk_digest_ctx *dctx, void *sig, size_t *len)
{
	struct apk_bearssl_digest *d = bdigest(dctx);
	struct apk_bearssl_pkey *k = bkey(d->pkey);
	unsigned char hash[64];
	size_t hlen = alg_len(d->alg);
	const br_rsa_private_key *sk;
	size_t siglen;

	if (!k || !k->is_priv || !hlen) return -APKE_SIGNATURE_GEN_FAILURE;
	sk = br_skey_decoder_get_rsa(&k->sk);
	if (!sk) return -APKE_SIGNATURE_GEN_FAILURE;
	siglen = (sk->n_bitlen + 7) / 8;
	if (*len < siglen) return -APKE_SIGNATURE_GEN_FAILURE;
	digest_out(d, hash);
	if (!br_rsa_i31_pkcs1_sign(alg_oid(d->alg), hash, hlen, sk, sig))
		return -APKE_SIGNATURE_GEN_FAILURE;
	*len = siglen;
	return 0;
}

int apk_verify_start(struct apk_digest_ctx *dctx, uint8_t alg, struct apk_pkey *pkey)
{
	struct apk_bearssl_digest *d = bdigest(dctx);
	struct apk_bearssl_pkey *k = bkey(pkey);
	if (!k || k->is_priv || !alg_len(alg)) return -APKE_CRYPTO_ERROR;
	d->pkey = pkey;
	digest_init(d, alg);
	dctx->alg = alg;
	return 0;
}

int apk_verify(struct apk_digest_ctx *dctx, void *sig, size_t len)
{
	struct apk_bearssl_digest *d = bdigest(dctx);
	struct apk_bearssl_pkey *k = bkey(d->pkey);
	unsigned char hash[64], out[64];
	size_t hlen = alg_len(d->alg);

	if (!k || k->is_priv || !hlen) return -APKE_SIGNATURE_INVALID;
	digest_out(d, hash);
	if (!br_rsa_i31_pkcs1_vrfy(sig, len, alg_oid(d->alg), hlen, &k->pub, out))
		return -APKE_SIGNATURE_INVALID;
	return memcmp(hash, out, hlen) == 0 ? 0 : -APKE_SIGNATURE_INVALID;
}

void apk_crypto_init(void)
{
}
