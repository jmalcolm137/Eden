pkgname = "wpa_supplicant"
pkgver = "2.11"
pkgrel = 6
makedepends = ["bearssl-devel", "bearssl-devel-static", "dbus-devel", "libnl", "libnl-devel", "linux-headers"]
pkgdesc = "WPA supplicant"
license = "BSD-3-Clause"
url = "https://w1.fi/wpa_supplicant"
source = f"https://w1.fi/releases/wpa_supplicant-{pkgver}.tar.gz"
sha256 = "912ea06f74e30a8e36fbb68064d6cdff218d8d591db0fc5d75dee6c81ac7fc0a"
# no test suite in the Oasis recipe
options = ["!check"]

_cflags = [
    "-include", "config.h",
    "-I.", "-Isrc", "-Isrc/utils", "-I/usr/include/libnl3",
    "-I/usr/include/dbus-1.0",
    "-I/usr/lib/dbus-1.0/include",
]

_common_sources = [
    "src/utils/common.c",
    "src/utils/eloop.c",
    "src/utils/os_unix.c",
    "src/utils/wpabuf.c",
    "src/utils/wpa_debug.c",
]

_wpa_sources = [
    "src/ap/wpa_auth.c",
    "src/ap/wpa_auth_ie.c",
    "src/ap/pmksa_cache_auth.c",
    "src/common/ctrl_iface_common.c",
    "src/common/hw_features_common.c",
    "src/common/ieee802_11_common.c",
    "src/common/ptksa_cache.c",
    "src/common/wpa_common.c",
    "src/crypto/aes-omac1.c",
    "src/crypto/aes-unwrap.c",
    "src/crypto/aes-wrap.c",
    "src/crypto/crypto_bearssl.c",
    "src/crypto/random.c",
    "src/crypto/rc4.c",
    "src/crypto/sha1-pbkdf2.c",
    "src/crypto/sha1-prf.c",
    "src/crypto/sha256-prf.c",
    "src/crypto/tls_none.c",
    "src/drivers/driver_common.c",
    "src/drivers/driver_nl80211.c",
    "src/drivers/driver_nl80211_capa.c",
    "src/drivers/driver_nl80211_event.c",
    "src/drivers/driver_nl80211_monitor.c",
    "src/drivers/driver_nl80211_scan.c",
    "src/drivers/drivers.c",
    "src/drivers/linux_ioctl.c",
    "src/drivers/netlink.c",
    "src/drivers/rfkill.c",
    "src/l2_packet/l2_packet_linux.c",
    "src/rsn_supp/pmksa_cache.c",
    "src/rsn_supp/preauth.c",
    "src/rsn_supp/wpa.c",
    "src/rsn_supp/wpa_ie.c",
    "src/utils/bitfield.c",
    "src/utils/config.c",
    "src/utils/crc32.c",
    "src/utils/ip_addr.c",
    "src/utils/radiotap.c",
    "wpa_supplicant/bssid_ignore.c",
    "wpa_supplicant/bss.c",
    "wpa_supplicant/config.c",
    "wpa_supplicant/config_file.c",
    "wpa_supplicant/ctrl_iface.c",
    "wpa_supplicant/ctrl_iface_unix.c",
    "wpa_supplicant/dbus/dbus_common.c",
    "wpa_supplicant/dbus/dbus_dict_helpers.c",
    "wpa_supplicant/dbus/dbus_new.c",
    "wpa_supplicant/dbus/dbus_new_handlers.c",
    "wpa_supplicant/dbus/dbus_new_helpers.c",
    "wpa_supplicant/eap_register.c",
    "wpa_supplicant/events.c",
    "wpa_supplicant/ibss_rsn.c",
    "wpa_supplicant/main.c",
    "wpa_supplicant/notify.c",
    "wpa_supplicant/op_classes.c",
    "wpa_supplicant/rrm.c",
    "wpa_supplicant/scan.c",
    "wpa_supplicant/sme.c",
    "wpa_supplicant/twt.c",
    "wpa_supplicant/wpa_supplicant.c",
    "wpa_supplicant/wpas_glue.c",
]

_wpa_cli_sources = [
    "src/common/cli.c",
    "src/common/wpa_ctrl.c",
    "src/utils/edit_simple.c",
    "wpa_supplicant/wpa_cli.c",
]


def pre_build(self):
    self.cp(self.files_path / "config.h", "config.h")


def build(self):
    from cbuild.util import compiler

    cc = compiler.C(self)
    self.mkdir("obj", parents=True)
    self.mkdir("out", parents=True)
    objs = []
    for src in _common_sources:
        obj = "obj/" + src.replace("/", "_").removesuffix(".c") + ".o"
        cc.invoke([src], obj, obj_file=True, flags=_cflags)
        objs.append(obj)
    self.do("ar", "rcs", "libcommon.a", *objs)

    cc.invoke(
        [*_wpa_sources, "libcommon.a"],
        "out/wpa_supplicant",
        flags=_cflags,
        ldflags=[
            "/usr/lib/libbearssl.a",
            "/usr/lib/libnl-3.a",
            "/usr/lib/libnl-genl-3.a",
            "-lm",
            "-lpthread",
            "-ldbus-1",
        ],
    )
    cc.invoke(
        [*_wpa_cli_sources, "libcommon.a"],
        "wpa_cli",
        flags=_cflags,
        ldflags=["-lpthread"],
    )


def install(self):
    self.install_bin("out/wpa_supplicant", name="wpa_supplicant")
    self.install_bin("wpa_cli")
    self.install_file(
        self.cwd / "wpa_supplicant/dbus/dbus-wpa_supplicant.conf",
        "usr/share/dbus-1/system.d",
        name="wpa_supplicant.conf",
    )
    self.install_file(
        self.files_path / "fi.w1.wpa_supplicant1.service",
        "usr/share/dbus-1/system-services",
    )
    self.install_man("wpa_supplicant/doc/docbook/wpa_supplicant.8")
    self.install_man("wpa_supplicant/doc/docbook/wpa_cli.8")
    self.install_man("wpa_supplicant/doc/docbook/wpa_supplicant.conf.5")
    self.install_license("COPYING")
