#!/usr/bin/env python3
"""生成公众号页眉图片"""
import argparse
import os
import sys
from typing import Optional

# 添加 scripts 目录到 path 以便导入 font_utils
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import font_utils

from PIL import Image, ImageDraw, ImageFont

def create_header(
    title: str = "默认公众号名称",
    slogan: str = "默认公众号 Slogan",
    output_path: str = "header.jpg",
    font_file: Optional[str] = None
):
    width = 900
    height = 120
    
    img = Image.new('RGB', (width, height), '#1a3a5c')
    draw = ImageDraw.Draw(img)
    
    try:
        actual_font_path = font_utils.find_chinese_font(preferred=font_file)
        title_font = ImageFont.truetype(actual_font_path, 42)
        sub_font = ImageFont.truetype(actual_font_path, 24)
        small_font = ImageFont.truetype(actual_font_path, 18)
    except FileNotFoundError as e:
        print(f"警告: 无法找到可用的中文字体，将使用默认字体。错误信息: {e}", file=sys.stderr)
        title_font = ImageFont.load_default()
        sub_font = ImageFont.load_default()
        small_font = ImageFont.load_default()

    # 左侧蓝色竖条装饰
    draw.rectangle([0, 0, 6, height], fill='#3daad6')

    # 小标签文字
    small_text = "ORIGINAL CONTENT"
    small_bbox = draw.textbbox((0, 0), small_text, font=small_font)
    small_w = small_bbox[2] - small_bbox[0]
    draw.text(((width - small_w) // 2, 14), small_text, fill='#7a9ab8', font=small_font)

    # 主标题
    title_bbox = draw.textbbox((0, 0), title, font=title_font)
    title_w = title_bbox[2] - title_bbox[0]
    draw.text(((width - title_w) // 2, 38), title, fill='#ffffff', font=title_font)

    # 分割线
    line_y = 90
    draw.rectangle([(width//2 - 20), line_y, (width//2 + 20), line_y + 2], fill='#3daad6')

    # slogan
    slogan_bbox = draw.textbbox((0, 0), slogan, font=sub_font)
    slogan_w = slogan_bbox[2] - slogan_bbox[0]
    draw.text(((width - slogan_w) // 2, 96), slogan, fill='#8ab0cc', font=sub_font)

    img.save(output_path, quality=95)
    print(f"Header saved: {output_path}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="生成公众号页眉图片")
    parser.add_argument("--title", default="默认公众号名称", help="公众号名称")
    parser.add_argument("--slogan", default="默认公众号 Slogan", help="公众号 Slogan")
    parser.add_argument("--output", default="header.jpg", help="输出文件路径")
    parser.add_argument("--font", default=None, help="字体文件路径（默认通过 font_utils 查找）")
    args = parser.parse_args()

    create_header(
        title=args.title,
        slogan=args.slogan,
        output_path=args.output,
        font_file=args.font
    )