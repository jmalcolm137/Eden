pkgname = "networkmanager"
pkgver = "1.51.4"
pkgrel = 2
build_style = "meson"
configure_args = [
    "-Dc_link_args=-Wl,--undefined-version",
    "-Dconfig_dhcp_default=internal",
    "-Dconfig_logging_backend_default=syslog",
    "-Dconfig_wifi_backend_default=wpa_supplicant",
    "-Dcrypto=gnutls",
    "-Ddbus_conf_dir=/usr/share/dbus-1/system.d",
    "-Ddocs=false",
    "-Debpf=false",
    "-Dintrospection=false",
    "-Dlibaudit=no",
    "-Dmodem_manager=false",
    "-Dnm_cloud_setup=false",
    "-Dnmtui=false",
    "-Dofono=false",
    "-Dovs=false",
    "-Dppp=false",
    "-Dqt=false",
    "-Dreadline=libedit",
    "-Dselinux=false",
    "-Dsession_tracking=no",
    "-Dsuspend_resume=consolekit",
    "-Dsystemd_journal=false",
    "-Dsystemdsystemunitdir=no",
    "-Dteamdctl=false",
    "-Dtests=no",
    "-Dudev_dir=/usr/lib/udev",
    "-Dvapi=false",
    "-Dwext=false",
]
meson_impl = "meson"
hostmakedepends = [
    "bash",
    "gettext",
    "libxslt-progs",
    "meson-real",
    "perl",
    "pkgconf",
    "python",
    "samurai",
]
makedepends = [
    "dbus-devel",
    "glib-devel",
    "gnutls-devel",
    "libcurl-devel",
    "libedit-readline-devel",
    "libndp-devel",
    "libpsl-devel",
    "libuuid-devel",
    "linux-headers",
    "polkit-devel",
    "udev-devel",
]
depends = ["dbus", "iproute2", "kmod", "perp", "wpa_supplicant"]
pkgdesc = "Network management daemon"
license = "GPL-2.0-or-later AND LGPL-2.1-or-later"
url = "https://gitlab.freedesktop.org/NetworkManager/NetworkManager"
source = f"https://download.gnome.org/sources/NetworkManager/1.51/NetworkManager-{pkgver}.tar.xz"
sha256 = "865a7cc5686a51d7efe81d7dcb3c5246bfa3b996a58629135354972804ff4d3c"
# libedit's readline compat has different callback signatures
tool_flags = {
    "CFLAGS": ["-Wno-incompatible-function-pointer-types"],
}
# tests need a live sysfs/dbus environment
options = ["etcfiles", "!check"]


@subpackage("networkmanager-devel")
def _(self):
    return self.default_devel()


@subpackage("networkmanager-libs")
def _(self):
    return self.default_libs()


def post_install(self):
    self.install_file(
        self.files_path / "NetworkManager.conf", "etc/NetworkManager"
    )
    # perp service; no 'down' file, so perpboot starts it by default
    self.install_file(
        self.files_path / "perp/networkmanager/rc",
        "etc/perp/networkmanager",
        mode=0o755,
        name="rc",
    )
    self.install_license("COPYING")
