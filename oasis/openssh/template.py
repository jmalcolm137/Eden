pkgname = "openssh"
pkgver = "10.6_p2"
pkgrel = 0
build_style = "gnu_configure"
configure_args = [
    "--with-ssl-dir=/usr",
    "--without-openssl-header-check",
    "--with-privsep-path=/var/empty",
    "--with-pid-dir=/run",
    "--with-maildir=/var/mail",
]
# let portable OpenSSH provide its own compat implementations
configure_env = {
    "ac_cv_func_freezero": "no",
    "ac_cv_func_recallocarray": "no",
    "ac_cv_func_timingsafe_bcmp": "no",
    "ac_cv_func_b64_ntop": "no",
    "ac_cv_func_b64_pton": "no",
    "ac_cv_func_arc4random": "no",
    "ac_cv_func_arc4random_buf": "no",
    "ac_cv_func_arc4random_uniform": "no",
    "ac_cv_func_strtonum": "no",
    "ac_cv_func_fmt_scaled": "no",
    "ac_cv_lib_util_fmt_scaled": "no",
    "ac_cv_have_decl_FMT_SCALED_STRSIZE": "no",
    "ac_cv_func_readpassphrase": "no",
    "ac_cv_have_decl_readpassphrase": "no",
    "ac_cv_func_scan_scaled": "no",
    "ac_cv_func_strmode": "no",
    "ac_cv_func_user_from_uid": "no",
    "ac_cv_func_group_from_gid": "no",
    "ac_cv_func_uid_from_user": "no",
    "ac_cv_func_gid_from_group": "no",
}
configure_gen = []
makedepends = ["libressl-devel", "zlib"]
pkgdesc = "OpenBSD Secure Shell"
license = "ISC"
url = "https://www.openssh.com"
source = (
    "https://cdn.openbsd.org/pub/OpenBSD/OpenSSH/portable/"
    f"openssh-{pkgver.replace('_', '')}.tar.gz"
)
sha256 = "9ae44872090cf2f06b3cf9ff147e7f16f309671340763ed2f99248398ae29d5b"
# no test suite in the Oasis recipe
options = ["etcfiles", "!check"]


def post_install(self):
    self.install_license("LICENCE")
    for name in ("ssh-keysign",):
        p = self.destdir / "usr/lib" / name
        if p.exists():
            p.chmod(0o755)
