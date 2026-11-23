pkgname = "firefox"
pkgver = "160.0.1"
pkgrel = 0
archs = ["x86_64"]
hostmakedepends = [
    "bash",
    "cargo-bootstrap",
    "cbindgen",
    "clang",
    "clang-libs",
    "gmake",
    "lld",
    "m4",
    "nasm",
    "nodejs",
    "perl",
    "pkgconf",
    "python",
    "rust",
    "unzip",
]
makedepends = [
    "alsa-lib-devel",
    "cairo-devel",
    "dbus-devel",
    "fontconfig-devel",
    "freetype-devel",
    "gdk-pixbuf-devel",
    "glib-devel",
    "gtk+3-devel",
    "harfbuzz-devel",
    "icu-devel",
    "libffi",
    "libjpeg-turbo-devel",
    "libnotify-devel",
    "libpulse-devel",
    "libxkbcommon-devel",
    "linux-headers",
    "mesa-devel",
    "pango-devel",
    "pipewire-devel",
    "pixman-devel",
    "wayland-devel",
    "zlib",
]
pkgdesc = "Firefox web browser"
license = "MPL-2.0 AND GPL-3.0-only AND LGPL-2.1-only AND LGPL-3.0-only"
url = "https://www.firefox.com"
source = (
    f"https://ftp.mozilla.org/pub/firefox/releases/{pkgver}/source/"
    f"firefox-{pkgver}.source.tar.xz"
)
sha256 = "7b9d95ddf24f7bbf5d0d05698bc02a66dac1eca438f80e093c5c76af7648b06d"
# The browser is installed into its own directory and loads its bundled
# libraries from there.
tool_flags = {"LDFLAGS": ["-Wl,-rpath=/usr/lib/firefox"]}
# Firefox has its own build and test harness
options = ["!check", "!lto"]


def _buildid(ts):
    # Mozilla wants a 14-digit UTC timestamp, but templates cannot import
    # anything outside cbuild.util.
    days, secs = divmod(ts, 86400)
    z = days + 719468
    era = (z if z >= 0 else z - 146096) // 146097
    doe = z - era * 146097
    yoe = (doe - doe // 1460 + doe // 36524 - doe // 146096) // 365
    year = yoe + era * 400
    doy = doe - (365 * yoe + yoe // 4 - yoe // 100)
    mp = (5 * doy + 2) // 153
    day = doy - (153 * mp + 2) // 5 + 1
    month = mp + 3 if mp < 10 else mp - 9
    if month <= 2:
        year += 1
    hour, rem = divmod(secs, 3600)
    minute, second = divmod(rem, 60)
    return (
        f"{year:04d}{month:02d}{day:02d}"
        f"{hour:02d}{minute:02d}{second:02d}"
    )


def _env(self):
    cwd = self.chroot_cwd
    return {
        "HOME": str(cwd / ".home"),
        "MOZBUILD_STATE_PATH": str(cwd / ".mozbuild"),
        "MOZCONFIG": str(cwd / "mozconfig"),
        "MOZ_OBJDIR": str(cwd / "obj"),
        "MOZ_BUILD_DATE": _buildid(self.source_date_epoch),
        "MOZ_APP_REMOTINGNAME": "firefox",
        "MOZ_NOSPAM": "1",
        "MOZILLA_OFFICIAL": "1",
        "BUILD_OFFICIAL": "1",
        "SHELL": "/bin/sh",
        "MACH_BUILD_PYTHON_NATIVE_PACKAGE_SOURCE": "none",
        "CARGO_BUILD_JOBS": "4",
        "CC": "/usr/bin/clang",
        "CXX": "/usr/bin/clang++",
        "RUST_TARGET": self.profile.triplet,
    }


def post_patch(self):
    self.mkdir(".home", parents=True)
    self.mkdir(".mozbuild", parents=True)
    text = (self.files_path / "mozconfig.in").read_text()
    text = text.replace("@TRIPLET@", self.profile.triplet)
    text = text.replace("@OBJDIR@", str(self.chroot_cwd / "obj"))
    (self.cwd / "mozconfig").write_text(text)


def configure(self):
    self.do("./mach", "configure", env=_env(self))


def build(self):
    self.do("./mach", "build", env=_env(self))


def install(self):
    env = _env(self)
    env["DESTDIR"] = self.chroot_destdir
    self.do("./mach", "install", env=env)

    self.install_file(
        self.files_path / "firefox.desktop", "usr/share/applications"
    )
    self.install_file(
        self.files_path / "vendor.js",
        "usr/lib/firefox/browser/defaults/preferences",
    )
    self.install_file(
        self.files_path / "distribution.ini", "usr/lib/firefox/distribution"
    )

    branding = self.cwd / "browser/branding/official"
    for png in branding.glob("default*.png"):
        size = png.stem.removeprefix("default")
        self.install_file(
            f"browser/branding/official/{png.name}",
            f"usr/share/icons/hicolor/{size}x{size}/apps",
            name="firefox.png",
        )
    self.install_file(
        "browser/branding/official/content/about-logo.svg",
        "usr/share/icons/hicolor/scalable/apps",
        name="firefox.svg",
    )

    self.install_license("LICENSE")
