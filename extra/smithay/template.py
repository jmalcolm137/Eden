pkgname = "smithay"
pkgver = "0.7.0"
pkgrel = 0
# xfwl4 4.21.1 pins this Smithay commit
_commit = "0a29aecf9e07a2227712ab470b0ab0ee56752272"
build_style = "cargo"
# Smithay is a Rust library, so there is no C ABI to build a shared object
# around.  Build the library with the features a compositor always needs; the
# resulting package installs the source tree for dependent packages to use as
# a path dependency.
make_build_args = [
    "-p",
    "smithay",
    "--no-default-features",
    "--features",
    "desktop,wayland_frontend",
]
# the renderer test harness is needed by the doctests
make_check_args = [
    "-p",
    "smithay",
    "--no-default-features",
    "--features",
    "desktop,wayland_frontend,renderer_gl,renderer_test",
]
hostmakedepends = ["cargo-bootstrap", "rust"]
pkgdesc = "Wayland compositor library"
license = "MIT"
url = "https://github.com/Smithay/smithay"
source = f"{url}/archive/{_commit}.tar.gz"
sha256 = "f00b38f6a0f9c32ecb696f5fb3d4f03e26d674f80365de891883352f3265b7ed"
# tests need a GPU and a running display
options = ["!check"]


def post_patch(self):
    # only the two library crates are shipped; drop the demo compositors from
    # the workspace so cargo does not resolve their much larger dependency
    # trees
    cf = self.cwd / "Cargo.toml"
    text = cf.read_text()
    members = """members = [
    "smithay-drm-extras",
    "smallvil",
    "anvil",
    "wlcs_anvil",
    "test_clients",
]"""

    if members not in text:
        self.error("unexpected workspace members in Cargo.toml")

    text = text.replace(members, 'members = ["smithay-drm-extras"]')

    # the examples and benches are not installed, so their target
    # declarations would point at missing files when used as a dependency
    start = text.index("[[example]]")
    end = text.index("[profile.release-with-debug]")
    text = text[:start] + text[end:]

    cf.write_text(text)


def install(self):
    # cargo source tree consumed by other packages with a path dependency,
    # e.g. xfwl4's
    #   smithay = { path = "/usr/share/cargo/registry/smithay-0.7.0" }
    #   smithay-drm-extras = {
    #       path = "/usr/share/cargo/registry/smithay-0.7.0/smithay-drm-extras",
    #   }
    reg = f"usr/share/cargo/registry/smithay-{pkgver}"

    self.install_dir(reg)
    for f in ["Cargo.toml", "build.rs", "LICENSE.txt", "README.md"]:
        self.install_file(f, reg)
    self.install_files("src", reg)
    self.install_files("smithay-drm-extras", reg)

    self.install_license("LICENSE.txt")
