#!/usr/bin/env python3
"""
生成微信公众号封面风格×配色预览拼图。

默认输出:
  tmp/wechat-cover-previews/cover-style-palette-preview-grid.jpg

用法:
  python3 create_cover_preview_grid.py
  python3 create_cover_preview_grid.py --title "封面预览" --output /path/to/grid.jpg
"""

import argparse
import os
import subprocess
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont


STYLES = ["minimal-grid", "card-editorial", "diagonal-motion", "soft-gradient"]
PALETTES = ["blue-tech", "purple-insight", "green-growth", "orange-energy", "rose-story", "slate-pro"]


def load_font(size: int):
    candidates = [
        "/System/Library/Fonts/Supplemental/PingFang.ttc",
        "/System/Library/Fonts/Supplemental/Arial Unicode.ttf",
    ]
    for fp in candidates:
        if os.path.exists(fp):
            try:
                return ImageFont.truetype(fp, size)
            except Exception:
                pass
    return ImageFont.load_default()


def generate_single_previews(skill_dir: Path, singles_dir: Path):
    create_cover = skill_dir / "scripts" / "create_cover.py"
    singles_dir.mkdir(parents=True, exist_ok=True)

    for s in STYLES:
        for p in PALETTES:
            out = singles_dir / f"{s}__{p}.jpg"
            cmd = [
                "python3",
                str(create_cover),
                "--title",
                "AI 创作提效",
                "--subtitle",
                f"{s} · {p}",
                "--style",
                s,
                "--palette",
                p,
                "--output",
                str(out),
            ]
            subprocess.run(cmd, check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)


def build_grid(singles_dir: Path, output: Path, title: str):
    cell_w, cell_h = 300, 128
    left_w = 210
    top_h = 140
    pad = 14

    W = left_w + pad + len(PALETTES) * (cell_w + pad) + pad
    H = top_h + pad + len(STYLES) * (cell_h + pad) + pad
    canvas = Image.new("RGB", (W, H), (245, 247, 250))
    draw = ImageDraw.Draw(canvas)

    font_title = load_font(40)
    font_sub = load_font(18)
    font_head = load_font(20)
    font_label = load_font(18)

    subtitle = "行=风格，列=配色，初次配置请选择默认风格"

    tb = draw.textbbox((0, 0), title, font=font_title)
    tw, th = tb[2] - tb[0], tb[3] - tb[1]
    draw.text(((W - tw) // 2, 18), title, fill=(20, 28, 45), font=font_title)

    sb = draw.textbbox((0, 0), subtitle, font=font_sub)
    sw, sh = sb[2] - sb[0], sb[3] - sb[1]
    draw.text(((W - sw) // 2, 18 + th + 8), subtitle, fill=(90, 100, 120), font=font_sub)

    header_y0 = top_h - 48
    header_y1 = top_h - 8
    for i, p in enumerate(PALETTES):
        x = left_w + pad + i * (cell_w + pad)
        draw.rounded_rectangle((x, header_y0, x + cell_w, header_y1), radius=8, fill=(230, 235, 242))
        pb = draw.textbbox((0, 0), p, font=font_head)
        pw, ph = pb[2] - pb[0], pb[3] - pb[1]
        draw.text((x + (cell_w - pw) / 2, header_y0 + (header_y1 - header_y0 - ph) / 2), p, fill=(40, 50, 75), font=font_head)

    for r, s in enumerate(STYLES):
        y = top_h + pad + r * (cell_h + pad)
        draw.rounded_rectangle((pad, y, left_w - 10, y + cell_h), radius=10, fill=(230, 235, 242))
        lb = draw.textbbox((0, 0), s, font=font_label)
        lh = lb[3] - lb[1]
        draw.text((20, y + (cell_h - lh) / 2), s, fill=(40, 50, 75), font=font_label)

        for c, p in enumerate(PALETTES):
            x = left_w + pad + c * (cell_w + pad)
            img = Image.open(singles_dir / f"{s}__{p}.jpg").convert("RGB").resize((cell_w, cell_h))
            canvas.paste(img, (x, y))
            draw.rectangle((x, y, x + cell_w, y + cell_h), outline=(210, 216, 228), width=1)

    output.parent.mkdir(parents=True, exist_ok=True)
    canvas.save(output, quality=92)


def main():
    parser = argparse.ArgumentParser(description="生成封面风格×配色预览拼图")
    parser.add_argument("--title", default="微信公众号封面预览（风格 × 配色）", help="拼图标题")
    parser.add_argument("--output", default="", help="输出路径")
    args = parser.parse_args()

    skill_dir = Path(__file__).resolve().parent.parent
    workspace = skill_dir.parent.parent  # /workspace

    base = workspace / "tmp" / "wechat-cover-previews"
    singles = base / "singles"

    output = Path(args.output).resolve() if args.output else (base / "cover-style-palette-preview-grid.jpg")

    generate_single_previews(skill_dir, singles)
    build_grid(singles, output, args.title)

    print(output)


if __name__ == "__main__":
    main()
