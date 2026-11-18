pkgname = "xfwl4"
pkgver = "4.21.1"
pkgrel = 0
# extra/smithay carries this source; use it instead of the git dependency
# (keep the version in sync with extra/smithay)
_smithay_version = "0.7.0"
_smithay_commit = "0a29aecf9e07a2227712ab470b0ab0ee56752272"
_smithay_dir = f"/usr/share/cargo/registry/smithay-{_smithay_version}"
build_style = "cargo"
# Wayland only: no nested X11/winit backend; the xwayland feature is needed
# by upstream's unconditionally compiled shell code but is never started
make_build_args = [
    "-p",
    "xfwl4",
    "--no-default-features",
    "--features",
    "udev,egl,gettext-system,xwayland",
]
make_check_args = [*make_build_args]
hostmakedepends = [
    "cargo-bootstrap",
    "gettext",
    "pkgconf",
    "rust",
]
# libinput >= 1.28, libxfce4ui >= 4.21.4 (libxfce4kbd-private-3),
# pixman >= 0.44 and xfconf >= 4.21.2 are required by the Cargo features
makedepends = [
    "cairo-devel",
    "gdk-pixbuf-devel",
    "glib-devel",
    "gtk+3-devel",
    "libdisplay-info-devel",
    "libdrm-devel",
    "libinput-devel",
    "libseat-devel",
    "libxfce4ui-devel",
    "libxkbcommon-devel",
    "mesa-gbm-devel",
    "pango-devel",
    "pixman-devel",
    "smithay",
    "udev-devel",
    "wayland-devel",
    "xfconf-devel",
]
depends = [
    "dbus",
    "xfwm4-themes",
]
pkgdesc = "Xfce Wayland compositor"
license = "GPL-3.0-or-later"
url = "https://gitlab.xfce.org/xfce/xfwl4"
source = f"https://archive.xfce.org/src/xfce/xfwl4/4.21/xfwl4-{pkgver}.tar.xz"
sha256 = "fee9a4777009bdbee160fd9e247d99060a26ef933e942303f7689d19cf6441ff"
# build.rs bakes these into the binary
env = {
    "PREFIX": "/usr",
    "SYSCONFDIR": "/etc",
    "BINDIR": "/usr/bin",
    "DATADIR": "/usr/share",
    "PKGDATADIR": "/usr/share/xfce4/xfwl4",
    "LOCALEDIR": "/usr/share/locale",
}


def _linguas(self):
    return [
        line.strip()
        for line in (self.cwd / "po/LINGUAS").read_text().splitlines()
        if line.strip() and not line.startswith("#")
    ]


def post_patch(self):
    cf = self.cwd / "Cargo.toml"
    text = cf.read_text()

    # only build the compositor, not the test clients
    members = """members = [
    ".",
    "test-clients",
]"""

    if members not in text:
        self.error("unexpected workspace members in Cargo.toml")
    text = text.replace(members, 'members = ["."]')

    # use the packaged Smithay source tree rather than fetching the pinned
    # git dependency
    for dep, path in [
        ("smithay", _smithay_dir),
        ("smithay-drm-extras", f"{_smithay_dir}/smithay-drm-extras"),
    ]:
        old = f"""[dependencies.{dep}]
git = "https://github.com/smithay/smithay"
rev = "{_smithay_commit}"
"""
        new = f"""[dependencies.{dep}]
path = "{path}"
"""

        if old not in text:
            self.error(f"unexpected {dep} dependency in Cargo.toml")
        text = text.replace(old, new)

    cf.write_text(text)


    # the Rust sources use the xwayland feature unconditionally in the shell
    # and focus code; build with it but never start Xwayland
    mp = self.cwd / "src/main.rs"
    mtext = mp.read_text()
    block = """    #[cfg(feature = "xwayland")]
    {
        match state.start_xwayland(None) {
            Ok(display_number) => {
                // SAFETY: This may not be safe, as other threads have been started, and we can't be sure
                // what they are doing.
                unsafe {
                    std::env::set_var("DISPLAY", format!(":{display_number}"));
                }
            }
            Err(err) => tracing::warn!("Xwayland failed to start; X11 clients will not work: {err}"),
        }
    }

"""
    if block not in mtext:
        self.error("unexpected Xwayland startup block in main.rs")
    mp.write_text(mtext.replace(block, ""))


def post_build(self):
    # upstream's meson build compiles the gettext catalogs and merges the
    # desktop entry; generate the catalogs and install the untranslated entry
    for lang in _linguas(self):
        self.mkdir(f"locale/{lang}/LC_MESSAGES", parents=True)
        self.do(
            "msgfmt",
            "-o",
            f"locale/{lang}/LC_MESSAGES/xfwl4.mo",
            f"po/{lang}.po",
        )


def install(self):
    from cbuild.util import cargo

    self.install_bin(cargo.target_path(self, "xfwl4"))
    self.install_file(
        "resources/xfwl4.desktop.in",
        "usr/share/wayland-sessions",
        name="xfwl4.desktop",
    )
    self.install_file("resources/defaults", "usr/share/xfce4/xfwl4")
    self.install_files("locale", "usr/share")
    self.install_license("LICENSE")
