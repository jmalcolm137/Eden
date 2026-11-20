pkgname = "xfce4-cpufreq-plugin"
pkgver = "1.3.0"
pkgrel = 0
build_style = "meson"
hostmakedepends = [
    "gettext",
    "glib-devel",
    "muon",
    "pkgconf",
    "samurai",
]
makedepends = [
    "gtk+3-devel",
    "libxfce4ui-devel",
    "libxfce4util-devel",
    "xfce4-panel-devel",
]
pkgdesc = "Xfce CPU governor and frequency panel plugin"
license = "GPL-2.0-or-later"
url = "https://docs.xfce.org/panel-plugins/xfce4-cpufreq-plugin/start"
source = "https://archive.xfce.org/src/panel-plugins/xfce4-cpufreq-plugin/1.3/xfce4-cpufreq-plugin-1.3.0.tar.xz"
sha256 = "baa5b90f72e8c262777f1e246acae125af489e2c168a5f7f890d9d2b5567ec20"
# upstream tests need a display and a running session bus
options = ["!check"]
