#ifndef APK_BEARSSL_TLS_H
#define APK_BEARSSL_TLS_H

#include <sys/types.h>

struct fetch_tls;

struct fetch_tls *fetch_tls_new(int fd, const char *host, int verify, int verbose);
ssize_t fetch_tls_read(struct fetch_tls *tls, void *buf, size_t len);
ssize_t fetch_tls_write(struct fetch_tls *tls, const void *buf, size_t len);
void fetch_tls_free(struct fetch_tls *tls);

#endif
