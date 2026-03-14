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
from typing import Dict, Optional, Tuple

# 添加 scripts 目录到 path 以便导入 font_utils
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import font_utils


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

    # Calculate text bounding box more accurately
    # For multiline text, `textbbox` returns a box for the whole block.
    # We need to split lines and get individual line widths for proper centering.
    title_lines = title.split('\n')
    max_title_width = 0
    for line in title_lines:
        bbox = draw.textbbox((0, 0), line, font=font_large)
        max_title_width = max(max_title_width, bbox[2] - bbox[0])
    
    current_y = title_y - (len(title_lines) - 1) * font_large.size / 2 # Adjust starting Y for multi-line title

    for line in title_lines:
        bbox = draw.textbbox((0, 0), line, font=font_large)
        tw = bbox[2] - bbox[0]
        tx = (w - tw) / 2
        draw.text((tx, current_y), line, fill=palette["text"], font=font_large)
        current_y += font_large.size # Move to next line

    if subtitle:
        subtitle_lines = subtitle.split('\n')
        current_y = sub_y - (len(subtitle_lines) - 1) * font_small.size / 2
        for line in subtitle_lines:
            bbox2 = draw.textbbox((0, 0), line, font=font_small)
            tw2 = bbox2[2] - bbox2[0]
            tx2 = (w - tw2) / 2
            draw.text((tx2, current_y), line, fill=palette["sub"], font=font_small)
            current_y += font_small.size


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


def render_html_cover(
    template_path: str,
    output_path: str,
    title: str,
    subtitle: str,
    account_name: str,
    slogan: str,
    tag: str,
):
    """
    使用 Playwright 渲染 HTML 模板并截图。
    """
    from playwright.sync_api import sync_playwright
    from jinja2 import Environment, FileSystemLoader

    template_dir = os.path.dirname(template_path)
    template_filename = os.path.basename(template_path)

    env = Environment(loader=FileSystemLoader(template_dir))
    template = env.get_template(template_filename)

    # 渲染 HTML 模板
    rendered_html = template.render(
        title=title,
        subtitle=subtitle,
        account_name=account_name,
        slogan=slogan,
        tag=tag,
    )
    
    # 写入临时文件供 Playwright 读取
    # 确保 temp_cover.html 在 output_path 同一目录下，方便 Playwright 定位相对资源
    temp_html_path = os.path.join(os.path.dirname(output_path), "temp_cover.html")
    with open(temp_html_path, "w", encoding="utf-8") as f:
        f.write(rendered_html)

    try:
        with sync_playwright() as p:
            browser = p.chromium.launch()
            page = browser.new_page(viewport={"width": 900, "height": 383})
            # 使用 file:// 协议加载本地 HTML 文件
            page.goto("file://" + os.path.abspath(temp_html_path).replace("\\", "/"))
            page.wait_for_load_state("networkidle")
            page.wait_for_timeout(500)  # 留一些时间给字体加载和渲染
            page.screenshot(path=output_path, quality=95)
            browser.close()
    finally:
        if os.path.exists(temp_html_path):
            os.remove(temp_html_path)

def create_cover(
    title: str,
    subtitle: str,
    output: str,
    html_template_path: Optional[str],
    style: str,
    palette_name: str,
    rotate: str,
    seed: str,
    bg_override: Optional[str],
    text_override: Optional[str],
    sub_override: Optional[str],
    font_path: Optional[str],
    account_name: str = "",
    slogan: str = "",
    tag: str = "",
):
    from PIL import Image, ImageDraw, ImageFont

    if html_template_path:
        # 使用 HTML 模板渲染
        render_html_cover(
            template_path=html_template_path,
            output_path=output,
            title=title,
            subtitle=subtitle,
            account_name=account_name,
            slogan=slogan,
            tag=tag,
        )
        # HTML 模板不返回 palette 名称，返回模板名
        return os.path.basename(html_template_path)
    else:
        # 回退到 PIL 渲染
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

        # 使用 font_utils 查找字体
        try:
            actual_font_path = font_utils.find_chinese_font(preferred=font_path)
        except FileNotFoundError as e:
            raise RuntimeError(f"无法找到可用的中文字体: {e}")

        font_large = ImageFont.truetype(actual_font_path, 52)
        font_small = ImageFont.truetype(actual_font_path, 28)
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

    parser.add_argument("--font", default=None, help="字体文件路径（默认通过 font_utils 查找）")
    # HTML 模板相关参数
    parser.add_argument("--html-template", default=None, help="HTML 封面模板路径")
    parser.add_argument("--account-name", default="", help="公众号名称（用于 HTML 模板）")
    parser.add_argument("--slogan", default="", help="公众号 Slogan（用于 HTML 模板）")
    parser.add_argument("--tag", default="", help="分类标签（用于 HTML 模板）")

    args = parser.parse_args()

    if args.list_presets:
        print_presets()
        sys.exit(0)

    # 如果是 HTML 模板，标题可以从模板中来，所以不强制要求
    if not args.html_template and not args.title.strip():
        print("Error: --title is required unless using --list-presets or --html-template", file=sys.stderr)
        sys.exit(1)
    
    # 如果没有指定字体，font_utils 会自动查找
    if args.font is None and not args.html_template:
        # PIL 模式下默认使用 skill 目录下的字体
        skill_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        args.font = os.path.join(skill_dir, "assets", "NotoSansCJKsc-Bold.otf")


    try:
        seed = args.seed or args.title
        used_style_info = create_cover(
            title=args.title,
            subtitle=args.subtitle,
            output=args.output,
            html_template_path=args.html_template,
            style=args.style,
            palette_name=args.palette,
            rotate=args.rotate,
            seed=seed,
            bg_override=args.bg_color,
            text_override=args.text_color,
            sub_override=args.sub_color,
            font_path=args.font,
            account_name=args.account_name,
            slogan=args.slogan,
            tag=args.tag,
        )
        print(f"Cover saved: {args.output}")
        if args.html_template:
            print(f"Used HTML Template: {args.html_template}")
        else:
            print(f"Style: {args.style}")
            print(f"Palette: {used_style_info}")
    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)
