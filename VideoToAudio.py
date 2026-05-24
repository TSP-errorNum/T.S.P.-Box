#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
视频提取音频工具 (使用 moviepy)
需要安装: pip install moviepy
"""

import argparse
import sys
from pathlib import Path

try:
    from moviepy import __version__ as moviepy_version
    from moviepy import VideoFileClip
    print(f"[信息] 成功加载 moviepy，版本: {moviepy_version}")
except ImportError as e:
    print("=" * 60)
    print("错误：未找到 moviepy 库！")
    print("请在当前虚拟环境中执行：")
    print("    pip install moviepy")
    print("=" * 60)
    sys.exit(1)


def extract_audio(video_path: str, audio_path: str, bitrate: str = None) -> None:
    video_file = Path(video_path)
    if not video_file.exists():
        raise FileNotFoundError(f"视频文件不存在: {video_path}")

    out_ext = Path(audio_path).suffix.lower()

    # 根据扩展名选择编码器
    if out_ext == '.mp3':
        codec = 'libmp3lame'
        default_bitrate = '192k'
    elif out_ext == '.wav':
        codec = 'pcm_s16le'
        default_bitrate = None   # WAV 无损
    elif out_ext == '.m4a':
        codec = 'aac'
        default_bitrate = '128k'
    elif out_ext == '.ogg':
        codec = 'libvorbis'
        default_bitrate = '192k'
    else:
        raise ValueError(f"不支持的音频格式: {out_ext}，请使用 .mp3, .wav, .m4a, .ogg")

    final_bitrate = bitrate if bitrate else default_bitrate

    print(f"输入: {video_path}")
    print(f"输出: {audio_path}")
    print(f"编码: {codec}")
    if final_bitrate:
        print(f"比特率: {final_bitrate}")

    try:
        with VideoFileClip(str(video_file)) as video:
            audio = video.audio
            if audio is None:
                raise ValueError("视频没有音频轨道")

            # 关键修改：只保留通用参数，移除 verbose
            audio.write_audiofile(
                audio_path,
                bitrate=final_bitrate,
                codec=codec,
                logger=None      # 关闭进度条（若想显示可改为 'bar'）
            )
        print("✅ 提取完成！")
    except Exception as e:
        raise RuntimeError(f"提取失败: {e}")


def main():
    parser = argparse.ArgumentParser(description="从视频提取音频 (moviepy)")
    parser.add_argument("input", help="输入视频文件")
    parser.add_argument("output", help="输出音频文件 (.mp3/.wav/.m4a/.ogg)")
    parser.add_argument("--bitrate", "-b", default=None, help="比特率如 192k")
    args = parser.parse_args()

    try:
        extract_audio(args.input, args.output, args.bitrate)
    except Exception as err:
        print(f"\n❌ {err}")
        sys.exit(1)


if __name__ == "__main__":
    main()
