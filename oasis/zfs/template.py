pkgname = "zfs"
pkgver = "2.4.0"
pkgrel = 0
makedepends = [
    "bearssl-devel-static", "libtirpc-devel-static", "linux-headers",
    "util-linux-libs-static", "zlib-ng-compat-devel-static",
]
pkgdesc = "ZFS filesystem and tools"
license = "CDDL-1.0"
url = "https://openzfs.org"
source = "https://github.com/openzfs/zfs/releases/download/zfs-2.4.0/zfs-2.4.0.tar.gz"
sha256 = "7bdf13de0a71d95554c0e3e47d5e8f50786c30d4f4b63b7c593b1d11af75c9ee"
# userland tools only; no kernel modules
options = ["!check"]

_cflags = [
    "-std=c99", "-Wall", "-include", "config.h",
    "-D_GNU_SOURCE", "-D_LARGEFILE64_SOURCE",
    "-Iinclude", "-Imodule/icp/include", "-Ilib/libspl/include",
    "-Ilib/libspl/include/os/linux", "-Ilib/libshare", "-Ilib/libzfs_core",
    "-Ilib/libzpool/include", "-Ilib/libzutil", "-Icmd/zpool", "-I/usr/include/tirpc",
]

_libs = {}


def _ar(self, cc, name, srcs):
    objs = []
    for src in srcs:
        obj = "obj/" + src.replace("/", "_").removesuffix(".c") + ".o"
        cc.invoke([src], obj, obj_file=True, flags=_cflags)
        objs.append(obj)
    self.do("ar", "rcs", name, *objs)
    _libs[name] = objs


def pre_build(self):
    self.cp(self.template_path / "config.h", self.cwd / "config.h")
    self.cp(self.template_path / "bitutil.c", self.cwd / "bitutil.c")


def build(self):
    from cbuild.util import compiler

    cc = compiler.C(self)
    self.mkdir("obj", parents=True)

    _ar(self, cc, "libavl.a", ["module/avl/avl.c"])
    _ar(self, cc, "libshare.a", [
        "lib/libshare/libshare.c", "lib/libshare/nfs.c",
        "lib/libshare/os/linux/nfs.c", "lib/libshare/os/linux/smb.c",
    ])
    _ar(self, cc, "libspl.a", [
        "lib/libspl/assert.c", "lib/libspl/backtrace.c", "lib/libspl/atomic.c",
        "lib/libspl/getexecname.c", "lib/libspl/list.c", "lib/libspl/mkdirp.c",
        "lib/libspl/page.c", "lib/libspl/strlcat.c", "lib/libspl/strlcpy.c",
        "lib/libspl/timestamp.c", "lib/libspl/tunables.c",
        "lib/libspl/os/linux/getexecname.c", "lib/libspl/os/linux/gethostid.c",
        "lib/libspl/os/linux/getmntany.c", "lib/libspl/os/linux/zone.c",
    ])
    _ar(self, cc, "libtpool.a", ["lib/libtpool/thread_pool.c"])
    _ar(self, cc, "libefi.a", ["lib/libefi/rdwr_efi.c"])
    _ar(self, cc, "libnvpair.a", [
        "lib/libnvpair/libnvpair.c", "lib/libnvpair/libnvpair_json.c",
        "lib/libnvpair/nvpair_alloc_system.c",
        "module/nvpair/nvpair_alloc_fixed.c", "module/nvpair/nvpair.c",
        "module/nvpair/fnvpair.c",
    ])
    _ar(self, cc, "libzutil.a", [
        "lib/libzutil/zutil_device_path.c", "lib/libzutil/zutil_import.c",
        "lib/libzutil/zutil_nicenum.c", "lib/libzutil/zutil_pool.c",
        "lib/libzutil/os/linux/zutil_setproctitle.c",
        "lib/libzutil/os/linux/zutil_device_path_os.c",
        "lib/libzutil/os/linux/zutil_import_os.c",
    ])
    _ar(self, cc, "libuutil.a", [
        "lib/libuutil/uu_alloc.c", "lib/libuutil/uu_avl.c",
        "lib/libuutil/uu_ident.c", "lib/libuutil/uu_list.c",
        "lib/libuutil/uu_misc.c", "lib/libuutil/uu_string.c",
    ])
    _ar(self, cc, "libzfs_core.a", [
        "lib/libzfs_core/libzfs_core.c",
        "lib/libzfs_core/os/linux/libzfs_core_ioctl.c",
    ])
    _ar(self, cc, "libzfs.a", [
        "lib/libzfs/libzfs_changelist.c", "lib/libzfs/libzfs_config.c",
        "lib/libzfs/libzfs_crypto.c", "lib/libzfs/libzfs_dataset.c",
        "lib/libzfs/libzfs_diff.c", "lib/libzfs/libzfs_import.c",
        "lib/libzfs/libzfs_iter.c", "lib/libzfs/libzfs_mount.c",
        "lib/libzfs/libzfs_pool.c", "lib/libzfs/libzfs_sendrecv.c",
        "lib/libzfs/libzfs_status.c", "lib/libzfs/libzfs_util.c",
        "lib/libzfs/os/linux/libzfs_mount_os.c",
        "lib/libzfs/os/linux/libzfs_pool_os.c",
        "lib/libzfs/os/linux/libzfs_util_os.c",
        "module/zcommon/cityhash.c", "module/zcommon/zfeature_common.c",
        "module/zcommon/zfs_comutil.c", "module/zcommon/zfs_fletcher.c",
        "module/zcommon/zfs_fletcher_superscalar.c",
        "module/zcommon/zfs_fletcher_superscalar4.c",
        "module/zcommon/zfs_namecheck.c", "module/zcommon/zfs_prop.c",
        "module/zcommon/zfs_valstr.c", "module/zcommon/zpool_prop.c",
        "module/zcommon/zprop_common.c",
        "bitutil.c",
    ])

    group = [
        "libzfs.a", "libzfs_core.a", "libuutil.a", "libnvpair.a",
        "libshare.a", "libzutil.a", "libefi.a", "libspl.a", "libtpool.a",
        "libavl.a",
    ]
    link = ["-Wl,--start-group"] + group + [
        "-Wl,--end-group", "-lbearssl", "-lz", "-luuid", "-lblkid",
        "-ltirpc", "-lpthread", "-lm", "-ldl",
    ]

    cc.invoke([
        "cmd/zed/zed.c", "cmd/zed/zed_conf.c", "cmd/zed/zed_disk_event.c",
        "cmd/zed/zed_event.c", "cmd/zed/zed_exec.c", "cmd/zed/zed_file.c",
        "cmd/zed/zed_log.c", "cmd/zed/zed_strings.c",
        "cmd/zed/agents/fmd_api.c", "cmd/zed/agents/fmd_serd.c",
        "cmd/zed/agents/zfs_agents.c", "cmd/zed/agents/zfs_diagnosis.c",
        "cmd/zed/agents/zfs_mod.c", "cmd/zed/agents/zfs_retire.c",
    ], "zed", flags=_cflags, ldflags=link)
    cc.invoke([
        "cmd/zfs/zfs_iter.c", "cmd/zfs/zfs_main.c", "cmd/zfs/zfs_project.c",
    ], "zfs", flags=_cflags, ldflags=link)
    cc.invoke([
        "cmd/zpool/zpool_iter.c", "cmd/zpool/zpool_main.c",
        "cmd/zpool/zpool_util.c", "cmd/zpool/zpool_vdev.c",
        "cmd/zpool/os/linux/zpool_vdev_os.c",
    ], "zpool", flags=_cflags, ldflags=link)
    cc.invoke([
        "cmd/zstream/zstream.c", "cmd/zstream/zstream_dump.c",
        "cmd/zstream/zstream_redup.c", "cmd/zstream/zstream_token.c",
    ], "zstream", flags=_cflags, ldflags=link)

    with open(self.cwd / "zed.8", "w") as f:
        self.do(
            "sed", "-e", "s,@sysconfdir@,/etc,",
            "-e", "s,@zfsexecdir@,/libexec/zfs,",
            "-e", "s,@runstatedir@,/run,", "man/man8/zed.8.in", stdout=f,
        )


def install(self):
    for b in ("zed", "zfs", "zpool", "zstream"):
        self.install_bin(b)
    self.install_link("usr/bin/zstreamdump", "zstream")
    man8 = [
        "zfs", "zfs-allow", "zfs-bookmark", "zfs-change-key", "zfs-clone",
        "zfs-create", "zfs-destroy", "zfs-diff", "zfs-get", "zfs-groupspace",
        "zfs-hold", "zfs-inherit", "zfs-jail", "zfs-list", "zfs-load-key",
        "zfs-mount", "zfs-program", "zfs-project", "zfs-projectspace",
        "zfs-promote", "zfs-receive", "zfs-recv", "zfs-redact", "zfs-release",
        "zfs-rename", "zfs-rollback", "zfs-send", "zfs-set", "zfs-share",
        "zfs-snapshot", "zfs-unallow", "zfs-unjail", "zfs-unload-key",
        "zfs-unmount", "zfs-upgrade", "zfs-userspace", "zfs-wait", "zpool",
        "zpool-add", "zpool-attach", "zpool-checkpoint", "zpool-clear",
        "zpool-create", "zpool-destroy", "zpool-detach", "zpool-events",
        "zpool-export", "zpool-get", "zpool-history", "zpool-import",
        "zpool-initialize", "zpool-iostat", "zpool-labelclear", "zpool-list",
        "zpool-offline", "zpool-online", "zpool-reguid", "zpool-remove",
        "zpool-reopen", "zpool-replace", "zpool-resilver", "zpool-scrub",
        "zpool-set", "zpool-split", "zpool-status", "zpool-sync",
        "zpool-trim", "zpool-upgrade", "zpool-wait", "zstream", "zstreamdump",
    ]
    for m in man8:
        self.install_man(f"man/man8/{m}.8")
    self.install_man("zed.8")
    self.install_man("man/man4/zfs.4")
    for m in ["zfsconcepts", "zfsprops", "zpool-features", "zpoolconcepts", "zpoolprops"]:
        self.install_man(f"man/man7/{m}.7")
    self.install_license("LICENSE")
