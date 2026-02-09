#!/usr/bin/env python3
"""
生成公众号封面图。
用法: python3 create_cover.py --title "主标题" --subtitle "副标题" --output cover.jpg
可选: --bg-color "235,240,248" --text-color "40,50,75"
"""
import argparse
import os
import sys

def create_cover(title, subtitle, output, bg_color, text_color, sub_color, font_path):
    from PIL import Image, ImageDraw, ImageFont

    width, height = 900, 383

    bg = tuple(int(c) for c in bg_color.split(','))
    tc = tuple(int(c) for c in text_color.split(','))
    sc = tuple(int(c) for c in sub_color.split(','))

    img = Image.new('RGB', (width, height), color=bg)
    draw = ImageDraw.Draw(img)

    # 浅格子纹理
    grid_r = max(0, bg[0] - 17)
    grid_g = max(0, bg[1] - 15)
    grid_b = max(0, bg[2] - 10)
    grid_color = (grid_r, grid_g, grid_b)
    grid_spacing = 40

    for x in range(0, width, grid_spacing):
        draw.line([(x, 0), (x, height)], fill=grid_color, width=1)
    for y in range(0, height, grid_spacing):
        draw.line([(0, y), (width, y)], fill=grid_color, width=1)

    # 对角线装饰
    accent_r = max(0, bg[0] - 35)
    accent_g = max(0, bg[1] - 30)
    accent_b = max(0, bg[2] - 20)
    accent_color = (accent_r, accent_g, accent_b)

    for i in range(5):
        offset = 60 * i
        draw.line([(width - 200 + offset, height), (width, height - 200 + offset)], fill=accent_color, width=2)
    for i in range(5):
        offset = 60 * i
        draw.line([(0, 200 - offset), (200 - offset, 0)], fill=accent_color, width=2)

    # 加载字体
    if not os.path.exists(font_path):
        print(f"Error: Font not found at {font_path}", file=sys.stderr)
        sys.exit(1)

    font_large = ImageFont.truetype(font_path, 52)
    font_small = ImageFont.truetype(font_path, 28)

    # 标题居中
    bbox = draw.textbbox((0, 0), title, font=font_large)
    tw = bbox[2] - bbox[0]
    tx = (width - tw) / 2
    ty = height / 2 - 55
    draw.text((tx, ty), title, fill=tc, font=font_large)

    # 副标题居中
    if subtitle:
        bbox2 = draw.textbbox((0, 0), subtitle, font=font_small)
        tw2 = bbox2[2] - bbox2[0]
        tx2 = (width - tw2) / 2
        ty2 = height / 2 + 20
        draw.text((tx2, ty2), subtitle, fill=sc, font=font_small)

    img.save(output, 'JPEG', quality=95)
    print(f"Cover saved: {output}")


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='生成公众号封面图')
    parser.add_argument('--title', required=True, help='主标题')
    parser.add_argument('--subtitle', default='', help='副标题')
    parser.add_argument('--output', default='cover.jpg', help='输出文件路径')
    parser.add_argument('--bg-color', default='235,240,248', help='背景色 R,G,B')
    parser.add_argument('--text-color', default='40,50,75', help='标题文字色 R,G,B')
    parser.add_argument('--sub-color', default='90,100,130', help='副标题文字色 R,G,B')
    parser.add_argument('--font', default=None, help='字体文件路径（默认使用 assets 目录下的思源黑体）')
    args = parser.parse_args()

    # 默认字体路径：skill assets 目录
    if args.font is None:
        skill_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        args.font = os.path.join(skill_dir, 'assets', 'NotoSansCJKsc-Bold.otf')

    create_cover(args.title, args.subtitle, args.output, args.bg_color, args.text_color, args.sub_color, args.font)
