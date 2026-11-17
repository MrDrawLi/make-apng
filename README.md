# make-apng

把文件夹里的 PNG 合成 APNG（动画 PNG）的小脚本，基于 Pillow，无其他依赖。

## 安装

```bash
pip install pillow
```

## 用法

```bash
python make_apng.py                  # 合成当前文件夹所有 PNG → apng.png
python make_apng.py D:/frames        # 指定文件夹
python make_apng.py -o result.png    # 指定输出名
python make_apng.py -d 200           # 每帧 200ms
python make_apng.py --fps 12         # 按帧率换算时长
python make_apng.py -l 3             # 循环 3 次（默认 0 = 无限循环）
```

## 特性

- **自然排序**：`frame2` 排在 `frame10` 前面（文件名数字按数值比较）
- **尺寸不一致**：自动缩放到第一帧尺寸并提示
- **色彩模式不一致**：自动统一（RGB / RGBA / P 等）
- **防自吞**：输出文件不会误当成输入帧
- 兼容 Chrome / Edge / Firefox / Safari

## 环境要求

Python 3.8+，Pillow 8.3+（APNG 支持）
