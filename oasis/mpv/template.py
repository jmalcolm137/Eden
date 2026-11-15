pkgname = "mpv"
pkgver = "0.38.0"
pkgrel = 0
_commit = "02254b92dd237f03aa0a151c2a68778c4ea848f9"
makedepends = [
    "ffmpeg-devel", "libass-devel", "libplacebo-devel", "linux-headers",
    "zlib-static",
]
pkgdesc = "Media player"
license = "GPL-2.0-or-later"
url = "https://mpv.io"
source = f"https://github.com/mpv-player/mpv/archive/{_commit}.tar.gz"
sha256 = "dad9517224f0cbf257f1476f8609743b73edcf0a8d5333dd7ab81166e306ad9f"
# reduced feature set: ffmpeg, zlib and terminal output only
options = ["!check"]

_sources = [
    'audio/aframe.c',
    'audio/chmap.c',
    'audio/chmap_sel.c',
    'audio/decode/ad_lavc.c',
    'audio/decode/ad_spdif.c',
    'audio/filter/af_drop.c',
    'audio/filter/af_format.c',
    'audio/filter/af_lavcac3enc.c',
    'audio/filter/af_scaletempo.c',
    'audio/filter/af_scaletempo2.c',
    'audio/filter/af_scaletempo2_internals.c',
    'audio/fmt-conversion.c',
    'audio/format.c',
    'audio/out/ao.c',
    'audio/out/ao_lavc.c',
    'audio/out/ao_null.c',
    'audio/out/ao_pcm.c',
    'audio/out/buffer.c',
    'common/av_common.c',
    'common/av_log.c',
    'common/codecs.c',
    'common/common.c',
    'common/encode_lavc.c',
    'common/msg.c',
    'common/playlist.c',
    'common/recorder.c',
    'common/stats.c',
    'common/tags.c',
    'common/version.c',
    'demux/codec_tags.c',
    'demux/cue.c',
    'demux/cache.c',
    'demux/demux.c',
    'demux/demux_cue.c',
    'demux/demux_disc.c',
    'demux/demux_edl.c',
    'demux/demux_lavf.c',
    'demux/demux_mf.c',
    'demux/demux_mkv.c',
    'demux/demux_mkv_timeline.c',
    'demux/demux_null.c',
    'demux/demux_playlist.c',
    'demux/demux_raw.c',
    'demux/demux_timeline.c',
    'demux/ebml.c',
    'demux/packet.c',
    'demux/timeline.c',
    'filters/f_async_queue.c',
    'filters/f_autoconvert.c',
    'filters/f_auto_filters.c',
    'filters/f_decoder_wrapper.c',
    'filters/f_demux_in.c',
    'filters/f_hwtransfer.c',
    'filters/f_lavfi.c',
    'filters/f_output_chain.c',
    'filters/f_swresample.c',
    'filters/f_swscale.c',
    'filters/f_utils.c',
    'filters/filter.c',
    'filters/frame.c',
    'filters/user_filters.c',
    'input/cmd.c',
    'input/event.c',
    'input/input.c',
    'input/ipc.c',
    'input/keycodes.c',
    'misc/bstr.c',
    'misc/charset_conv.c',
    'misc/dispatch.c',
    'misc/io_utils.c',
    'misc/json.c',
    'misc/language.c',
    'misc/natural_sort.c',
    'misc/node.c',
    'misc/path_utils.c',
    'misc/random.c',
    'misc/rendezvous.c',
    'misc/thread_pool.c',
    'misc/thread_tools.c',
    'options/m_config_core.c',
    'options/m_config_frontend.c',
    'options/m_option.c',
    'options/m_property.c',
    'options/options.c',
    'options/parse_commandline.c',
    'options/parse_configfile.c',
    'options/path.c',
    'player/audio.c',
    'player/client.c',
    'player/command.c',
    'player/configfiles.c',
    'player/external_files.c',
    'player/loadfile.c',
    'player/main.c',
    'player/misc.c',
    'player/osd.c',
    'player/playloop.c',
    'player/screenshot.c',
    'player/scripting.c',
    'player/sub.c',
    'player/video.c',
    'stream/cookies.c',
    'stream/stream.c',
    'stream/stream_avdevice.c',
    'stream/stream_cb.c',
    'stream/stream_concat.c',
    'stream/stream_edl.c',
    'stream/stream_file.c',
    'stream/stream_lavf.c',
    'stream/stream_memory.c',
    'stream/stream_mf.c',
    'stream/stream_null.c',
    'stream/stream_slice.c',
    'sub/ass_mp.c',
    'sub/dec_sub.c',
    'sub/draw_bmp.c',
    'sub/filter_sdh.c',
    'sub/img_convert.c',
    'sub/lavc_conv.c',
    'sub/osd.c',
    'sub/osd_libass.c',
    'sub/sd_ass.c',
    'sub/sd_lavc.c',
    'video/csputils.c',
    'video/decode/vd_lavc.c',
    'video/filter/refqueue.c',
    'video/filter/vf_format.c',
    'video/filter/vf_sub.c',
    'video/fmt-conversion.c',
    'video/hwdec.c',
    'video/image_loader.c',
    'video/image_writer.c',
    'video/img_format.c',
    'video/mp_image.c',
    'video/mp_image_pool.c',
    'video/out/aspect.c',
    'video/out/bitmap_packer.c',
    'video/out/dither.c',
    'video/out/dr_helper.c',
    'video/out/filter_kernels.c',
    'video/out/gpu/hwdec.c',
    'video/out/libmpv_sw.c',
    'video/out/vo.c',
    'video/out/vo_image.c',
    'video/out/vo_lavc.c',
    'video/out/vo_libmpv.c',
    'video/out/vo_null.c',
    'video/out/vo_tct.c',
    'video/out/vo_kitty.c',
    'video/out/win_state.c',
    'video/repack.c',
    'video/sws_utils.c',
    'osdep/io.c',
    'osdep/semaphore-mac.c',
    'osdep/subprocess.c',
    'osdep/timer.c',
    'ta/ta.c',
    'ta/ta_talloc.c',
    'ta/ta_utils.c',
    'osdep/language-posix.c',
    'osdep/subprocess-posix.c',
    'osdep/threads-posix.c',
    'osdep/path-unix.c',
    'osdep/terminal-unix.c',
    'osdep/timer-linux.c',
    'input/ipc-unix.c',
    'osdep/poll_wrapper.c',
    'sub/filter_regex.c',
    'audio/chmap_avchannel.c',
]

_incs = [
    'etc/input.conf',
    'etc/builtin.conf',
    'sub/osd_font.otf',
    'player/lua/defaults.lua',
    'player/lua/assdraw.lua',
    'player/lua/options.lua',
    'player/lua/osc.lua',
    'player/lua/ytdl_hook.lua',
    'player/lua/stats.lua',
    'player/lua/console.lua',
    'player/lua/auto_profiles.lua',
    'player/lua/input.lua',
]

_cflags = ["-D_GNU_SOURCE", "-I."]


def pre_build(self):
    self.cp(self.files_path / "config.h", self.cwd / "config.h")
    self.cp(self.template_path / "file2string.c", self.cwd / "file2string.c")
    self.cp(self.template_path / "version.awk", self.cwd / "version.awk")


def build(self):
    from cbuild.util import compiler

    cc = compiler.C(self)
    cc.invoke(["file2string.c"], "file2string", flags=["-std=c99", "-D_GNU_SOURCE"])
    with open(self.cwd / "version.h", "w") as f:
        self.do("awk", "-f", "version.awk", "VERSION", stdout=f)
    for src in _incs:
        out = src + ".inc"
        (self.cwd / out).parent.mkdir(parents=True, exist_ok=True)
        self.do("./file2string", src, stdout=open(self.cwd / out, "w"))
    cc.invoke(
        ["osdep/main-fn-unix.c", *_sources], "mpv", flags=_cflags,
        ldflags=[
            "-lavcodec", "-lavdevice", "-lavfilter", "-lavformat",
            "-lavutil", "-lswresample", "-lswscale", "-lplacebo", "-lass", "-lz", "-lpthread",
            "-lm", "-ldl",
        ],
    )


def install(self):
    self.install_bin("mpv")
    self.install_man(self.template_path / "mpv.1")
    self.install_license("LICENSE.GPL")
