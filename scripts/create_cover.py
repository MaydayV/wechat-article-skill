#!/usr/bin/env python3
"""
生成公众号封面图（支持风格 × 配色预设）。

基础用法:
  python3 create_cover.py --title "主标题" --subtitle "副标题" --output cover.jpg

预设用法:
  python3 create_cover.py --title "主标题" --style minimal-grid --palette blue-tech --output cover.jpg

查看可用预设:
  python3 create_cover.py --list-presets

兼容旧参数:
  --bg-color / --text-color / --sub-color 仍可覆盖预设颜色。
"""
import argparse
import os
import random
import sys
from typing import Dict, Tuple


def clamp(v: int) -> int:
    return max(0, min(255, v))


def darken(color: Tuple[int, int, int], delta: int) -> Tuple[int, int, int]:
    return tuple(clamp(c - delta) for c in color)


def lighten(color: Tuple[int, int, int], delta: int) -> Tuple[int, int, int]:
    return tuple(clamp(c + delta) for c in color)


def parse_rgb(text: str) -> Tuple[int, int, int]:
    try:
        parts = [int(x.strip()) for x in text.split(",")]
        if len(parts) != 3:
            raise ValueError("RGB must have 3 components")
        return tuple(clamp(x) for x in parts)
    except Exception as e:
        raise ValueError(f"Invalid RGB '{text}': {e}")


PALETTES: Dict[str, Dict[str, Tuple[int, int, int]]] = {
    "blue-tech": {
        "bg": (234, 242, 255),
        "text": (30, 58, 138),
        "sub": (59, 130, 246),
        "accent1": (147, 197, 253),
        "accent2": (96, 165, 250),
        "card": (255, 255, 255),
    },
    "purple-insight": {
        "bg": (243, 232, 255),
        "text": (91, 33, 182),
        "sub": (124, 58, 237),
        "accent1": (196, 181, 253),
        "accent2": (167, 139, 250),
        "card": (255, 255, 255),
    },
    "green-growth": {
        "bg": (236, 253, 243),
        "text": (22, 101, 52),
        "sub": (5, 150, 105),
        "accent1": (110, 231, 183),
        "accent2": (52, 211, 153),
        "card": (255, 255, 255),
    },
    "orange-energy": {
        "bg": (255, 247, 237),
        "text": (154, 52, 18),
        "sub": (234, 88, 12),
        "accent1": (253, 186, 116),
        "accent2": (251, 146, 60),
        "card": (255, 255, 255),
    },
    "rose-story": {
        "bg": (255, 241, 242),
        "text": (159, 18, 57),
        "sub": (225, 29, 72),
        "accent1": (253, 164, 175),
        "accent2": (251, 113, 133),
        "card": (255, 255, 255),
    },
    "slate-pro": {
        "bg": (248, 250, 252),
        "text": (15, 23, 42),
        "sub": (51, 65, 85),
        "accent1": (148, 163, 184),
        "accent2": (100, 116, 139),
        "card": (255, 255, 255),
    },
}

STYLES = [
    "minimal-grid",
    "card-editorial",
    "diagonal-motion",
    "soft-gradient",
]


def style_minimal_grid(draw, w, h, palette):
    grid_color = darken(palette["bg"], 12)
    spacing = 40
    for x in range(0, w, spacing):
        draw.line([(x, 0), (x, h)], fill=grid_color, width=1)
    for y in range(0, h, spacing):
        draw.line([(0, y), (w, y)], fill=grid_color, width=1)

    accent = darken(palette["accent1"], 20)
    for i in range(5):
        off = 60 * i
        draw.line([(w - 200 + off, h), (w, h - 200 + off)], fill=accent, width=2)
        draw.line([(0, 200 - off), (200 - off, 0)], fill=accent, width=2)


def style_card_editorial(draw, w, h, palette):
    # background dots
    dot = lighten(palette["accent1"], 15)
    for x in range(40, w, 36):
        for y in range(36, h, 36):
            draw.ellipse((x, y, x + 2, y + 2), fill=dot)

    # card + shadow
    card_w, card_h = int(w * 0.78), int(h * 0.62)
    x0 = (w - card_w) // 2
    y0 = (h - card_h) // 2
    x1 = x0 + card_w
    y1 = y0 + card_h

    shadow = darken(palette["accent2"], 25)
    draw.rounded_rectangle((x0 + 8, y0 + 10, x1 + 8, y1 + 10), radius=24, fill=shadow)
    draw.rounded_rectangle((x0, y0, x1, y1), radius=24, fill=palette["card"])

    # corner label
    ribbon = palette["accent2"]
    draw.rounded_rectangle((x0 + 20, y0 - 16, x0 + 190, y0 + 24), radius=10, fill=ribbon)


def style_diagonal_motion(draw, w, h, palette):
    # broad diagonal bands
    band1 = lighten(palette["accent1"], 8)
    band2 = lighten(palette["accent2"], 16)
    draw.polygon([(0, h), (w * 0.45, h), (w, h * 0.35), (w, h), (0, h)], fill=band1)
    draw.polygon([(0, h * 0.7), (w * 0.3, h * 0.7), (w, h * 0.12), (w, h * 0.26), (0, h * 0.84)], fill=band2)

    # top-left accents
    accent = darken(palette["accent2"], 18)
    for i in range(6):
        y = 26 + i * 14
        draw.line([(24, y), (220, y - 18)], fill=accent, width=2)


def style_soft_gradient(img, draw, w, h, palette):
    # vertical + slight horizontal gradient
    from PIL import Image

    overlay = Image.new("RGB", (w, h))
    px = overlay.load()
    top = lighten(palette["bg"], 8)
    bottom = darken(palette["bg"], 10)
    right_boost = lighten(palette["accent1"], 20)

    for y in range(h):
        t = y / max(1, h - 1)
        for x in range(w):
            r = int(top[0] * (1 - t) + bottom[0] * t)
            g = int(top[1] * (1 - t) + bottom[1] * t)
            b = int(top[2] * (1 - t) + bottom[2] * t)
            # subtle right glow
            k = x / max(1, w - 1)
            r = int(r * (1 - 0.08 * k) + right_boost[0] * (0.08 * k))
            g = int(g * (1 - 0.08 * k) + right_boost[1] * (0.08 * k))
            b = int(b * (1 - 0.08 * k) + right_boost[2] * (0.08 * k))
            px[x, y] = (clamp(r), clamp(g), clamp(b))

    img.paste(overlay)

    # soft circles
    c1 = lighten(palette["accent1"], 30)
    c2 = lighten(palette["accent2"], 25)
    draw.ellipse((w - 220, -70, w + 80, 210), fill=c1)
    draw.ellipse((-120, h - 190, 220, h + 120), fill=c2)


def draw_title_block(draw, w, h, title, subtitle, style, palette, font_large, font_small):
    # text layout differs slightly by style
    if style == "card-editorial":
        title_y = h // 2 - 55
        sub_y = h // 2 + 16
    else:
        title_y = h // 2 - 58
        sub_y = h // 2 + 18

    bbox = draw.textbbox((0, 0), title, font=font_large)
    tw = bbox[2] - bbox[0]
    tx = (w - tw) / 2
    draw.text((tx, title_y), title, fill=palette["text"], font=font_large)

    if subtitle:
        bbox2 = draw.textbbox((0, 0), subtitle, font=font_small)
        tw2 = bbox2[2] - bbox2[0]
        tx2 = (w - tw2) / 2
        draw.text((tx2, sub_y), subtitle, fill=palette["sub"], font=font_small)


def pick_palette(name: str, strategy: str, seed: str):
    keys = list(PALETTES.keys())
    if name != "auto":
        if name not in PALETTES:
            raise ValueError(f"Unknown palette: {name}")
        return name, PALETTES[name]

    if strategy == "sequential":
        # stable by seed hash
        idx = abs(hash(seed)) % len(keys)
        k = keys[idx]
        return k, PALETTES[k]

    # random
    k = random.choice(keys)
    return k, PALETTES[k]


def create_cover(title, subtitle, output, style, palette_name, rotate, seed, bg_override, text_override, sub_override, font_path):
    from PIL import Image, ImageDraw, ImageFont

    if style not in STYLES:
        raise ValueError(f"Unknown style: {style}")

    selected_palette_name, palette = pick_palette(palette_name, rotate, seed)
    palette = dict(palette)

    # compatible overrides
    if bg_override:
        palette["bg"] = parse_rgb(bg_override)
    if text_override:
        palette["text"] = parse_rgb(text_override)
    if sub_override:
        palette["sub"] = parse_rgb(sub_override)

    width, height = 900, 383
    img = Image.new("RGB", (width, height), color=palette["bg"])
    draw = ImageDraw.Draw(img)

    if style == "minimal-grid":
        style_minimal_grid(draw, width, height, palette)
    elif style == "card-editorial":
        style_card_editorial(draw, width, height, palette)
    elif style == "diagonal-motion":
        style_diagonal_motion(draw, width, height, palette)
    elif style == "soft-gradient":
        style_soft_gradient(img, draw, width, height, palette)

    if not os.path.exists(font_path):
        raise FileNotFoundError(f"Font not found: {font_path}")

    font_large = ImageFont.truetype(font_path, 52)
    font_small = ImageFont.truetype(font_path, 28)
    draw_title_block(draw, width, height, title, subtitle, style, palette, font_large, font_small)

    img.save(output, "JPEG", quality=95)
    return selected_palette_name


def print_presets():
    print("Styles:")
    for s in STYLES:
        print(f"- {s}")
    print("\nPalettes:")
    for p in PALETTES.keys():
        print(f"- {p}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="生成公众号封面图")
    parser.add_argument("--title", required=False, default="", help="主标题")
    parser.add_argument("--subtitle", default="", help="副标题")
    parser.add_argument("--output", default="cover.jpg", help="输出文件路径")

    # new options
    parser.add_argument("--style", default="minimal-grid", choices=STYLES, help="封面风格")
    parser.add_argument("--palette", default="auto", help="配色名（或 auto）")
    parser.add_argument("--rotate", default="sequential", choices=["sequential", "random"], help="当 palette=auto 时的选色策略")
    parser.add_argument("--seed", default="", help="配色轮换 seed（默认使用标题）")
    parser.add_argument("--list-presets", action="store_true", help="打印所有风格与配色")

    # backward-compatible color overrides
    parser.add_argument("--bg-color", default=None, help="覆盖背景色 R,G,B")
    parser.add_argument("--text-color", default=None, help="覆盖标题文字色 R,G,B")
    parser.add_argument("--sub-color", default=None, help="覆盖副标题文字色 R,G,B")

    parser.add_argument("--font", default=None, help="字体文件路径（默认 assets/NotoSansCJKsc-Bold.otf）")
    args = parser.parse_args()

    if args.list_presets:
        print_presets()
        sys.exit(0)

    if not args.title.strip():
        print("Error: --title is required unless using --list-presets", file=sys.stderr)
        sys.exit(1)

    if args.font is None:
        skill_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        args.font = os.path.join(skill_dir, "assets", "NotoSansCJKsc-Bold.otf")

    try:
        seed = args.seed or args.title
        used_palette = create_cover(
            title=args.title,
            subtitle=args.subtitle,
            output=args.output,
            style=args.style,
            palette_name=args.palette,
            rotate=args.rotate,
            seed=seed,
            bg_override=args.bg_color,
            text_override=args.text_color,
            sub_override=args.sub_color,
            font_path=args.font,
        )
        print(f"Cover saved: {args.output}")
        print(f"Style: {args.style}")
        print(f"Palette: {used_palette}")
    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)
