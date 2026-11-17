#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
把文件夹里的 PNG 合成 APNG（动画 PNG）

用法:
    python make_apng.py                     # 合成当前文件夹
    python make_apng.py D:/frames           # 指定文件夹
    python make_apng.py -o result.png       # 指定输出文件名
    python make_apng.py -d 200              # 每帧 200ms
    python make_apng.py --fps 12            # 按帧率 12fps 换算时长
    python make_apng.py -l 3                # 循环 3 次（0 = 无限循环）

帧顺序: 按文件名自然排序（frame2 < frame10）
"""

import argparse
import re
import sys
from pathlib import Path

try:
    from PIL import Image
except ImportError:
    sys.exit("需要 Pillow: pip install pillow")


def natural_key(path: Path):
    """自然排序: 把文件名里的数字按数值比较, frame2 排在 frame10 前面"""
    parts = re.split(r"(\d+)", path.name.lower())
    return [int(p) if p.isdigit() else p for p in parts]


def collect_pngs(folder: Path, exclude: set[str]) -> list[Path]:
    files = [p for p in folder.glob("*.png") if p.resolve() not in exclude]
    return sorted(files, key=natural_key)


def main():
    parser = argparse.ArgumentParser(description="把文件夹里的 PNG 合成 APNG")
    parser.add_argument("folder", nargs="?", default=".", help="PNG 所在文件夹（默认当前目录）")
    parser.add_argument("-o", "--output", default="apng.png", help="输出文件名（默认 apng.png）")
    parser.add_argument("-d", "--duration", type=int, default=100, help="每帧时长/毫秒（默认 100）")
    parser.add_argument("--fps", type=float, help="按帧率指定时长（覆盖 -d，如 --fps 12）")
    parser.add_argument("-l", "--loop", type=int, default=0, help="循环次数，0 表示无限循环（默认 0）")
    args = parser.parse_args()

    folder = Path(args.folder).resolve()
    if not folder.is_dir():
        sys.exit(f"文件夹不存在: {folder}")

    output = folder / args.output
    files = collect_pngs(folder, exclude={output.resolve()})

    if len(files) < 1:
        sys.exit(f"{folder} 下没有找到 PNG 文件")
    if len(files) == 1:
        print("警告: 只找到 1 张 PNG，输出将是没有动画的单帧 APNG")

    if args.fps:
        duration = round(1000 / args.fps)
        print(f"按帧率 {args.fps}fps → 每帧 {duration}ms")
    else:
        duration = args.duration

    frames = []
    base_size = None
    base_mode = None
    for f in files:
        im = Image.open(f)
        if base_size is None:
            base_size, base_mode = im.size, im.mode
        # 尺寸/模式不一致时统一到第一帧
        if im.size != base_size:
            print(f"警告: {f.name} 尺寸 {im.size} != {base_size}，已缩放对齐")
            im = im.resize(base_size, Image.LANCZOS)
        if im.mode != base_mode:
            print(f"警告: {f.name} 模式 {im.mode} != {base_mode}，已转换")
            im = im.convert(base_mode)
        frames.append(im)

    frames[0].save(
        output,
        save_all=True,
        append_images=frames[1:],
        duration=duration,
        loop=args.loop,
    )

    size_kb = output.stat().st_size / 1024
    print(f"已生成 {output.name}: {len(frames)} 帧, {base_size[0]}x{base_size[1]}, "
          f"每帧 {duration}ms, 循环 {'无限' if args.loop == 0 else args.loop} 次, {size_kb:.1f} KB")
    print("帧顺序: " + " → ".join(f.name for f in files))


if __name__ == "__main__":
    main()
