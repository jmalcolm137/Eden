/* Minimal BearSSL TLS client for apk-tools libfetch */

#include <errno.h>
#include <fcntl.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <time.h>
#include <unistd.h>

#include <bearssl.h>

#include "bearssl_tls.h"

#ifndef CA_CERT_FILE
#define CA_CERT_FILE "/etc/ssl/certs/ca-certificates.crt"
#endif

struct buf {
	unsigned char *p;
	size_t len, cap;
};

struct fetch_tls {
	br_ssl_client_context sc;
	br_x509_minimal_context xc;
	br_sslio_context ioc;
	unsigned char *iobuf;
	int fd;
};

static struct buf pem;
static struct buf dn;

static void buf_add(struct buf *b, const void *src, size_t len)
{
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

static void pem_add(void *ctx, const void *src, size_t len)
{
	buf_add(ctx, src, len);
}

static void dn_add(void *ctx, const void *src, size_t len)
{
	buf_add(ctx, src, len);
}

static unsigned char *dup_bytes(const unsigned char *p, size_t len)
{
	unsigned char *r = malloc(len ? len : 1);
	if (r && len) memcpy(r, p, len);
	return r;
}

static br_x509_trust_anchor *anchors;
static size_t anchors_num;

static int add_cert(const unsigned char *der, size_t len)
{
	br_x509_decoder_context xd;
	br_x509_pkey *pk;
	br_x509_trust_anchor *ta;
	size_t nc = anchors_num + 1;
	br_x509_trust_anchor *na;

	dn.len = 0;
	br_x509_decoder_init(&xd, dn_add, &dn);
	br_x509_decoder_push(&xd, der, len);
	if (br_x509_decoder_last_error(&xd) != 0) return 0;
	pk = br_x509_decoder_get_pkey(&xd);
	if (!pk) return 0;

	na = realloc(anchors, nc * sizeof *na);
	if (!na) return -1;
	anchors = na;
	ta = &anchors[anchors_num];
	memset(ta, 0, sizeof *ta);
	ta->dn.data = dup_bytes(dn.p, dn.len);
	ta->dn.len = dn.len;
	ta->flags = BR_X509_TA_CA;
	ta->pkey.key_type = pk->key_type;
	if (pk->key_type == BR_KEYTYPE_RSA) {
		ta->pkey.key.rsa.n = dup_bytes(pk->key.rsa.n, pk->key.rsa.nlen);
		ta->pkey.key.rsa.nlen = pk->key.rsa.nlen;
		ta->pkey.key.rsa.e = dup_bytes(pk->key.rsa.e, pk->key.rsa.elen);
		ta->pkey.key.rsa.elen = pk->key.rsa.elen;
	} else if (pk->key_type == BR_KEYTYPE_EC) {
		ta->pkey.key.ec.q = dup_bytes(pk->key.ec.q, pk->key.ec.qlen);
		ta->pkey.key.ec.qlen = pk->key.ec.qlen;
		ta->pkey.key.ec.curve = pk->key.ec.curve;
	} else {
		return 0;
	}
	anchors_num++;
	return 0;
}

static int load_anchors(void)
{
	static int done;
	const char *paths[] = { CA_CERT_FILE, "/etc/ssl/certs/ca-certificates.crt", "/etc/ssl/cert.pem", NULL };
	FILE *f = NULL;
	unsigned char *data;
	long sz;
	size_t off = 0;
	br_pem_decoder_context pc;

	if (done) return anchors_num > 0 ? 0 : -1;
	done = 1;
	for (int i = 0; paths[i]; i++) {
		f = fopen(paths[i], "rb");
		if (f) break;
	}
	if (!f) return -1;
	fseek(f, 0, SEEK_END);
	sz = ftell(f);
	fseek(f, 0, SEEK_SET);
	if (sz <= 0 || sz > 8 * 1024 * 1024) { fclose(f); return -1; }
	data = malloc(sz);
	if (!data) { fclose(f); return -1; }
	if (fread(data, 1, sz, f) != (size_t)sz) { fclose(f); free(data); return -1; }
	fclose(f);

	br_pem_decoder_init(&pc);
	br_pem_decoder_setdest(&pc, pem_add, &pem);
	while (off < (size_t)sz) {
		size_t n = br_pem_decoder_push(&pc, data + off, sz - off);
		int ev;
		off += n;
		ev = br_pem_decoder_event(&pc);
		if (ev == BR_PEM_END_OBJ) {
			if (add_cert(pem.p, pem.len) < 0) {
				free(data);
				return -1;
			}
			pem.len = 0;
		} else if (ev == BR_PEM_ERROR) {
			break;
		}
		if (n == 0 && ev == 0) break;
	}
	free(data);
	free(pem.p);
	pem.p = NULL;
	pem.len = pem.cap = 0;
	return anchors_num > 0 ? 0 : -1;
}

static int sock_read(void *ctx, unsigned char *buf, size_t len)
{
	int fd = *(int *)ctx;
	ssize_t r;
	do {
		r = read(fd, buf, len);
	} while (r < 0 && errno == EINTR);
	if (r <= 0) return -1;
	return (int)r;
}

static int sock_write(void *ctx, const unsigned char *buf, size_t len)
{
	int fd = *(int *)ctx;
	size_t off = 0;
	while (off < len) {
		ssize_t w = write(fd, buf + off, len - off);
		if (w < 0) {
			if (errno == EINTR) continue;
			return -1;
		}
		if (w == 0) return -1;
		off += w;
	}
	return (int)off;
}

struct fetch_tls *fetch_tls_new(int fd, const char *host, int verify, int verbose)
{
	struct fetch_tls *tls;
	time_t now;
	uint32_t days, secs;

	(void)verify;
	(void)verbose;
	if (load_anchors() < 0) return NULL;
	tls = calloc(1, sizeof *tls);
	if (!tls) return NULL;
	tls->fd = fd;
	tls->iobuf = malloc(BR_SSL_BUFSIZE_BIDI);
	if (!tls->iobuf) { free(tls); return NULL; }

	br_ssl_client_init_full(&tls->sc, &tls->xc, anchors, anchors_num);
	br_ssl_engine_set_buffer(&tls->sc.eng, tls->iobuf, BR_SSL_BUFSIZE_BIDI, 1);
	now = time(NULL);
	days = (uint32_t)(now / 86400) + 719528;
	secs = (uint32_t)(now % 86400);
	br_x509_minimal_set_time(&tls->xc, days, secs);

	if (!br_ssl_client_reset(&tls->sc, host, 0)) goto err;
	br_sslio_init(&tls->ioc, &tls->sc.eng, sock_read, &tls->fd,
		sock_write, &tls->fd);
	if (br_sslio_flush(&tls->ioc) < 0) goto err;
	return tls;
err:
	free(tls->iobuf);
	free(tls);
	return NULL;
}

ssize_t fetch_tls_read(struct fetch_tls *tls, void *buf, size_t len)
{
	ssize_t r = br_sslio_read(&tls->ioc, buf, len);
	if (r < 0) {
		errno = EIO;
		return -1;
	}
	return r;
}

ssize_t fetch_tls_write(struct fetch_tls *tls, const void *buf, size_t len)
{
	if (br_sslio_write_all(&tls->ioc, buf, len) < 0 ||
	    br_sslio_flush(&tls->ioc) < 0) {
		errno = EIO;
		return -1;
	}
	return (ssize_t)len;
}

void fetch_tls_free(struct fetch_tls *tls)
{
	if (!tls) return;
	br_sslio_close(&tls->ioc);
	free(tls->iobuf);
	free(tls);
}
