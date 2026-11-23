pkgname = "squashfs-tools-ng"
pkgver = "1.1.3"
pkgrel = 0
makedepends = ["zlib", "zstd", "zstd-devel", "zstd-devel-static"]
pkgdesc = "Tools and libraries for squashfs filesystems"
license = "GPL-3.0-or-later"
url = "https://github.com/AgentD/squashfs-tools-ng"
source = f"{url}/archive/refs/tags/v{pkgver}.tar.gz"
sha256 = "4214083eb921b89d194e41697c31dc086c059518e51fe0ee4eee88318c19ad0d"
# no test suite in the Oasis recipe
options = ["!check"]

_cflags = [
    "-std=c99", "-Wall", "-Wpedantic", "-Wno-discarded-qualifiers",
    "-D_GNU_SOURCE", "-I.", "-Iinclude",
]

_util = [
    "lib/util/str_table.c", "lib/util/alloc.c", "lib/util/rbtree.c",
    "lib/util/array.c", "lib/util/xxhash.c", "lib/util/hash_table.c",
    "lib/util/threadpool_serial.c", "lib/util/is_memory_zero.c",
    "lib/util/threadpool.c",
]

_fstream = [
    "lib/fstream/ostream.c", "lib/fstream/printf.c",
    "lib/fstream/istream.c", "lib/fstream/get_line.c",
    "lib/fstream/compressor.c",
    "lib/fstream/compress/ostream_compressor.c",
    "lib/fstream/compress/gzip.c", "lib/fstream/compress/zstd.c",
    "lib/fstream/uncompress/istream_compressor.c",
    "lib/fstream/uncompress/autodetect.c",
    "lib/fstream/uncompress/gzip.c", "lib/fstream/uncompress/zstd.c",
    "lib/fstream/unix/ostream.c", "lib/fstream/unix/istream.c",
]

_fstree = [
    "lib/fstree/fstree.c", "lib/fstree/fstree_from_file.c",
    "lib/fstree/fstree_sort.c", "lib/fstree/hardlink.c",
    "lib/fstree/post_process.c", "lib/fstree/get_path.c",
    "lib/fstree/mknode.c", "lib/fstree/fstree_from_dir.c",
    "lib/fstree/add_by_path.c", "lib/fstree/get_by_path.c",
    "lib/fstree/source_date_epoch.c", "lib/fstree/canonicalize_name.c",
    "lib/fstree/filename_sane.c",
]

_sqfs = [
    "lib/sqfs/id_table.c", "lib/sqfs/super.c", "lib/sqfs/readdir.c",
    "lib/sqfs/xattr/xattr.c", "lib/sqfs/write_table.c", "lib/sqfs/meta_writer.c",
    "lib/sqfs/read_super.c", "lib/sqfs/meta_reader.c", "lib/sqfs/read_inode.c",
    "lib/sqfs/write_inode.c", "lib/sqfs/dir_writer.c",
    "lib/sqfs/xattr/xattr_reader.c", "lib/sqfs/read_table.c",
    "lib/sqfs/comp/compressor.c", "lib/sqfs/dir_reader.c", "lib/sqfs/read_tree.c",
    "lib/sqfs/inode.c", "lib/sqfs/xattr/xattr_writer.c",
    "lib/sqfs/xattr/xattr_writer_flush.c", "lib/sqfs/xattr/xattr_writer_record.c",
    "lib/sqfs/write_super.c", "lib/sqfs/data_reader.c",
    "lib/sqfs/block_processor/frontend.c", "lib/sqfs/block_processor/block_processor.c",
    "lib/sqfs/block_processor/backend.c", "lib/sqfs/frag_table.c",
    "lib/sqfs/block_writer.c", "lib/sqfs/misc.c", "lib/sqfs/unix/io_file.c",
    "lib/sqfs/comp/gzip.c", "lib/sqfs/comp/zstd.c",
]

_tar = [
    "lib/tar/read_header.c", "lib/tar/write_header.c", "lib/tar/number.c",
    "lib/tar/checksum.c", "lib/tar/cleanup.c", "lib/tar/read_sparse_map.c",
    "lib/tar/read_sparse_map_old.c", "lib/tar/base64.c", "lib/tar/urldecode.c",
    "lib/tar/padd_file.c", "lib/tar/record_to_memory.c", "lib/tar/pax_header.c",
    "lib/tar/read_sparse_map_new.c",
]

_common = [
    "lib/common/inode_stat.c", "lib/common/hardlink.c", "lib/common/print_version.c",
    "lib/common/data_reader_dump.c", "lib/common/compress.c", "lib/common/comp_opt.c",
    "lib/common/data_writer.c", "lib/common/get_path.c",
    "lib/common/data_writer_ostream.c", "lib/common/perror.c",
    "lib/common/mkdir_p.c", "lib/common/parse_size.c", "lib/common/print_size.c",
    "lib/common/writer/init.c", "lib/common/writer/cleanup.c",
    "lib/common/writer/serialize_fstree.c", "lib/common/writer/finish.c",
]

_tools = {
    "gensquashfs": ["bin/gensquashfs/mkfs.c", "bin/gensquashfs/options.c",
                    "bin/gensquashfs/selinux.c", "bin/gensquashfs/dirscan_xattr.c"],
    "rdsquashfs": ["bin/rdsquashfs/rdsquashfs.c", "bin/rdsquashfs/list_files.c",
                   "bin/rdsquashfs/options.c", "bin/rdsquashfs/restore_fstree.c",
                   "bin/rdsquashfs/describe.c", "bin/rdsquashfs/fill_files.c",
                   "bin/rdsquashfs/dump_xattrs.c", "bin/rdsquashfs/stat.c"],
    "sqfsdiff": ["bin/sqfsdiff/sqfsdiff.c", "bin/sqfsdiff/util.c",
                 "bin/sqfsdiff/options.c", "bin/sqfsdiff/compare_dir.c",
                 "bin/sqfsdiff/node_compare.c", "bin/sqfsdiff/compare_files.c",
                 "bin/sqfsdiff/super.c", "bin/sqfsdiff/extract.c"],
    "sqfs2tar": ["bin/sqfs2tar/sqfs2tar.c", "bin/sqfs2tar/options.c",
                 "bin/sqfs2tar/write_tree.c", "bin/sqfs2tar/xattr.c"],
    "tar2sqfs": ["bin/tar2sqfs/tar2sqfs.c", "bin/tar2sqfs/options.c",
                 "bin/tar2sqfs/process_tarball.c"],
}

_mans = [
    "bin/gensquashfs/gensquashfs.1", "bin/rdsquashfs/rdsquashfs.1",
    "bin/sqfsdiff/sqfsdiff.1", "bin/sqfs2tar/sqfs2tar.1", "bin/tar2sqfs/tar2sqfs.1",
]


def pre_build(self):
    self.cp(self.files_path / "config.h", "config.h")


def build(self):
    from cbuild.util import compiler

    cc = compiler.C(self)
    self.mkdir("obj", parents=True)

    def build_lib(name, sources):
        objs = []
        for src in sources:
            obj = "obj/" + src.replace("/", "_").removesuffix(".c") + ".o"
            cc.invoke([src], obj, obj_file=True, flags=_cflags)
            objs.append(obj)
        self.do("ar", "rcs", name, *objs)

    build_lib("libutil.a", _util)
    build_lib("libfstream.a", _fstream)
    build_lib("libfstree.a", _fstree)
    build_lib("libsquashfs.a", _sqfs)
    build_lib("libtar.a", _tar)
    build_lib("libcommon.a", _common)

    ldflags = [
        "libcommon.a", "libsquashfs.a", "libfstree.a",
        "libfstream.a", "libtar.a", "libutil.a",
        "/usr/lib/libz.a", "/usr/lib/libzstd.a", "-lpthread",
    ]
    for name, sources in _tools.items():
        cc.invoke(sources + ldflags, name, flags=_cflags)


def install(self):
    for name in _tools:
        self.install_bin(name)
    for man in _mans:
        self.install_man(man)
    self.install_license("COPYING.md")
