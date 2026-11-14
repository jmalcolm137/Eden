pkgname = "tinyemu"
pkgver = "20191221"
pkgrel = 2
makedepends = ["bearssl-devel-static", "curl", "linux-headers", "zlib-static"]
pkgdesc = "Tiny emulator for x86 and RISC-V"
license = "MIT"
url = "https://bellard.org/tinyemu"
source = "https://bellard.org/tinyemu/tinyemu-2019-12-21.tar.gz"
sha256 = "be8351f2121819b3172fcedce5cb1826fa12c87da1b7ed98f269d3e802a05555"
# no test suite in the Oasis recipe
options = ["!check"]

_cflags = [
    "-D_GNU_SOURCE",
    "-DCONFIG_FS_NET",
    "-DCONFIG_RISCV_MAX_XLEN=64",
    "-DCONFIG_SLIRP",
    "-DCONFIG_X86EMU",
    '-DCONFIG_VERSION="2019-12-21"',
    "-I.",
]

_sources = [
    "virtio.c", "pci.c", "fs.c", "cutils.c", "iomem.c", "simplefb.c",
    "json.c", "machine.c", "temu.c",
    "slirp/bootp.c", "slirp/ip_icmp.c", "slirp/mbuf.c", "slirp/slirp.c",
    "slirp/tcp_output.c", "slirp/cksum.c", "slirp/ip_input.c", "slirp/misc.c",
    "slirp/socket.c", "slirp/tcp_subr.c", "slirp/udp.c", "slirp/if.c",
    "slirp/ip_output.c", "slirp/sbuf.c", "slirp/tcp_input.c", "slirp/tcp_timer.c",
    "fs_disk.c", "fs_net.c", "fs_wget.c", "fs_utils.c", "block_net.c",
    "riscv_machine.c", "softfp.c",
    "x86_cpu.c", "x86_machine.c", "ide.c", "ps2.c", "vmmouse.c", "pckbd.c", "vga.c",
]


def build(self):
    from cbuild.util import compiler

    cc = compiler.C(self)
    self.mkdir("obj", parents=True)
    cc.invoke(["riscv_cpu.c"], "obj/riscv_cpu32.o", obj_file=True,
              flags=_cflags + ["-DMAX_XLEN=32"])
    cc.invoke(["riscv_cpu.c"], "obj/riscv_cpu64.o", obj_file=True,
              flags=_cflags + ["-DMAX_XLEN=64"])
    cc.invoke(
        _sources + ["obj/riscv_cpu32.o", "obj/riscv_cpu64.o"],
        "temu",
        flags=_cflags,
        ldflags=["/usr/lib/libbearssl.a", "/usr/lib/libcurl.a", "/usr/lib/libz.a", "-lpthread"],
    )


def install(self):
    self.install_bin("temu")
    self.install_license("MIT-LICENSE.txt")
