pkgname = "cosmic-store"
pkgver = "1.11.0"
pkgrel = 0
archs = ["x86_64"]
hostmakedepends = ["cargo-bootstrap", "git", "pkgconf", "rust"]
makedepends = ["glib-devel", "libxkbcommon-devel", "openssl", "wayland-devel"]
pkgdesc = "Application store for the COSMIC desktop environment"
license = "GPL-3.0-only"
url = "https://github.com/pop-os/cosmic-store"
source = f"https://github.com/pop-os/cosmic-store/archive/refs/tags/epoch-{pkgver}.tar.gz"
sha256 = "d8c95307e4a865ab4681a0be86fea98f82fb052ecc7bcea98fad2b8165c34e83"
# the test suite needs a running compositor
options = ["!check"]

_cargo_env = {
    "CARGO_HOME": "/cbuild_cache/cargo",
    "CARGO_NET_OFFLINE": "true",
}


def post_patch(self):
    # Rust 1.99 no longer infers this closure parameter through the
    # FuturesUnordered/oneshot chain.
    p = self.cwd / "src/backend/mod.rs"
    text = p.read_text()
    base = (
        "futures::stream::FuturesUnordered<"
        "tokio::sync::oneshot::Receiver<Option<(BackendName, Arc<dyn Backend>)>>>"
    )
    decl = "let backends = futures::stream::FuturesUnordered::new();"
    if text.count(decl) != 1:
        self.error("unexpected backend declaration")
    text = text.replace(decl, f"let backends: {base} = futures::stream::FuturesUnordered::new();", 1)
    old = ".map(move |value| async move {"
    new = (
        ".map(move |value: Result<Option<(BackendName, Arc<dyn Backend>)>, "
        "tokio::sync::oneshot::error::RecvError>| async move {"
    )
    if text.count(old) != 1:
        self.error("unexpected backend stream closure")
    p.write_text(text.replace(old, new, 1))


def prepare(self):
    self.do(
        "cargo",
        "fetch",
        "--locked",
        env={"CARGO_HOME": "/cbuild_cache/cargo"},
        allow_network=True,
    )


def build(self):
    # flatpak, logind and the systemd-scope integration are not used on Eden
    self.do(
        "cargo",
        "build",
        "--release",
        "--locked",
        "--no-default-features",
        "--features",
        "dbus-config,desktop,logind,notify,single-instance,wgpu,wayland,xdg-portal",
        env=_cargo_env,
    )


def install(self):
    appid = "com.system76.CosmicStore"

    self.install_bin("target/release/cosmic-store")

    desktop = self.cwd / "target/xdgen" / f"{appid}.desktop"
    if not desktop.is_file():
        desktop = self.cwd / "res" / f"{appid}.desktop"
    self.install_file(desktop.relative_to(self.cwd), "usr/share/applications")

    metainfo = self.cwd / "target/xdgen" / f"{appid}.metainfo.xml"
    if not metainfo.is_file():
        metainfo = self.cwd / "res" / f"{appid}.metainfo.xml"
    self.install_file(metainfo.relative_to(self.cwd), "usr/share/metainfo")

    icons = self.cwd / "res/icons/hicolor"
    for path in icons.rglob("*"):
        if path.is_file():
            rel = path.relative_to(icons)
            self.install_file(
                f"res/icons/hicolor/{rel}",
                f"usr/share/icons/hicolor/{rel.parent}",
            )

    self.install_license("LICENSE")
