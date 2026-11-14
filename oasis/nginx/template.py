pkgname = "nginx"
pkgver = "1.31.0"
pkgrel = 0
build_style = "makefile"
configure_args = [
    "--with-http_ssl_module",
    "--with-http_v2_module",
    "--with-http_gzip_static_module",
    "--with-pcre",
    "--sbin-path=/usr/bin/nginx",
    "--conf-path=/etc/nginx/nginx.conf",
    "--pid-path=/run/nginx.pid",
    "--lock-path=/run/nginx.lock",
    "--http-log-path=/var/log/nginx/access.log",
    "--error-log-path=/var/log/nginx/error.log",
    "--http-client-body-temp-path=/var/lib/nginx/tmp/client_body",
    "--http-proxy-temp-path=/var/lib/nginx/tmp/proxy",
    "--http-fastcgi-temp-path=/var/lib/nginx/tmp/fastcgi",
    "--http-uwsgi-temp-path=/var/lib/nginx/tmp/uwsgi",
    "--http-scgi-temp-path=/var/lib/nginx/tmp/scgi",
]
make_dir = "."
make_use_env = True
makedepends = [
    "libressl-devel",
    "libressl-devel-static",
    "linux-headers",
    "pcre-devel",
    "pcre-devel-static",
    "zlib-static",
]
pkgdesc = "HTTP and reverse proxy server"
license = "BSD-2-Clause"
url = "https://nginx.org"
source = f"{url}/download/nginx-{pkgver}.tar.gz"
sha256 = "6d5b00d45393af2e4e7c52a442d2a198f0ccbc7678ed062a46f403edd833ebaa"
# no test suite in the Oasis recipe
options = ["etcfiles", "!check"]


def configure(self):
    self.do("./configure", "--prefix=/usr", *self.configure_args)



def post_install(self):
    self.install_license("LICENSE")
