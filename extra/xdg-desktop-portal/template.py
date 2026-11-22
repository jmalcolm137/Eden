pkgname = "xdg-desktop-portal"
pkgver = "1.22.1"
pkgrel = 0
archs = ["x86_64"]
build_style = "meson"
configure_args = [
    "-Ddocumentation=disabled",
    "-Dflatpak-interfaces=disabled",
    "-Dgeoclue=disabled",
    "-Dgudev=disabled",
    "-Dinstalled-tests=false",
    "-Dman-pages=disabled",
    "-Dsandboxed-image-validation=disabled",
    "-Dsandboxed-sound-validation=disabled",
    "-Dsystemd=disabled",
    "-Dtests=disabled",
]
hostmakedepends = ["gettext", "git", "meson-real", "pkgconf", "samurai"]
makedepends = [
    "fuse3-devel",
    "gdk-pixbuf-devel",
    "glib-devel",
    "gst-plugins-base-devel",
    "gstreamer-devel",
    "json-glib-devel",
    "pipewire-devel",
]
pkgdesc = "Portal frontend service for desktop integration"
license = "LGPL-2.1-or-later"
url = "https://github.com/flatpak/xdg-desktop-portal"
source = [
    f"https://github.com/flatpak/xdg-desktop-portal/archive/refs/tags/{pkgver}.tar.gz",
    "https://github.com/GNOME/gvdb/archive/c6f2359cc1d00f16e0a0e2527fa0bc1882b8b5ab.tar.gz>gvdb-src.tar.gz",
    "https://github.com/GNOME/libglnx/archive/ff64d52116ae74f0d25e24f089db28921ea171ff.tar.gz>libglnx-src.tar.gz",
]
source_paths = [".", "gvdb-src", "libglnx-src"]
sha256 = [
    "5afeda953c3743efaa1160e73d62c5bfcac2ceca60e0e134e9b48ed651783625",
    "14f082f122eb4e495e2ac96f235efb01525ae5d4a1f0fd98148b4f7c7f95ccd2",
    "fcf7670f61f003ae290ed8486814dc89bbe50eebb0bd5f56a77ebccc6ddefc94",
]
# the test suite needs a running session and portal backends
options = ["!check"]


def post_patch(self):
    # gvdb and libglnx are meson wraps.  The build root's git has no HTTPS
    # transport, so unpack the pinned revisions from source tarballs instead.
    for name, path in [("gvdb", "gvdb-src"), ("libglnx", "libglnx-src")]:
        dest = f"subprojects/{name}"
        self.rm(dest, recursive=True, force=True)
        self.cp(path, dest, recursive=True)

    # musl already declares these; drop libglnx's private fallbacks.
    p = self.cwd / "subprojects/libglnx/glnx-missing-syscall.h"
    text = p.read_text()
    text = text.replace("#if !HAVE_DECL_RENAMEAT2", "#if 0")
    text = text.replace(
        "#if !HAVE_DECL_NAME_TO_HANDLE_AT && defined(__NR_name_to_handle_at)",
        "#if 0",
    )
    p.write_text(text)


def post_install(self):
    # The session units are not used: portals are D-Bus activated.
    self.rm(self.destdir / "usr/lib/systemd", recursive=True, force=True)
    self.install_license("COPYING")
