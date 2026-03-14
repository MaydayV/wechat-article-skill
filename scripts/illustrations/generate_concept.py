#!/usr/bin/env python3
"""
生成概念示意图（通用版）。

用法:
  python3 generate_concept.py --title "核心概念" --left-label "你" --left-desc "战略·创意·决策" \
    --right-label "AI" --right-desc "执行·流程·标准化" --result "一家公司的全链路能力" --output concept.jpg
"""
import argparse
import os
import sys
from typing import Optional

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import font_utils

from PIL import Image, ImageDraw, ImageFont


def create_concept(
    title: str = "概念 = A + B",
    left_label: str = "A",
    left_desc: str = "描述A",
    right_label: str = "B",
    right_desc: str = "描述B",
    result: str = "最终结果",
    output_path: str = "concept.jpg",
    font_file: Optional[str] = None,
):
    width = 1200
    height = 800

    img = Image.new("RGB", (width, height), "white")
    draw = ImageDraw.Draw(img)

    try:
        actual_font_path = font_utils.find_chinese_font(preferred=font_file)
        title_font = ImageFont.truetype(actual_font_path, 56)
        subtitle_font = ImageFont.truetype(actual_font_path, 36)
        text_font = ImageFont.truetype(actual_font_path, 32)
    except FileNotFoundError:
        title_font = ImageFont.load_default()
        subtitle_font = ImageFont.load_default()
        text_font = ImageFont.load_default()

    # 背景渐变效果（简化版）
    for y in range(height):
        color_value = int(245 + (255 - 245) * (y / height))
        draw.line([(0, y), (width, y)], fill=(color_value, color_value, 255))

    # 标题
    title_bbox = draw.textbbox((0, 0), title, font=title_font)
    title_width = title_bbox[2] - title_bbox[0]
    draw.text(((width - title_width) // 2, 80), title, fill="#1a73e8", font=title_font)

    # 左侧
    person_x = 250
    person_y = 350
    draw.ellipse(
        [person_x - 80, person_y - 80, person_x + 80, person_y + 80],
        fill="#4CAF50",
        outline="#2E7D32",
        width=4,
    )
    text_bbox = draw.textbbox((0, 0), left_label, font=subtitle_font)
    text_width = text_bbox[2] - text_bbox[0]
    text_height = text_bbox[3] - text_bbox[1]
    draw.text(
        (person_x - text_width // 2, person_y - text_height // 2),
        left_label,
        fill="white",
        font=subtitle_font,
    )
    desc_bbox = draw.textbbox((0, 0), left_desc, font=text_font)
    desc_w = desc_bbox[2] - desc_bbox[0]
    draw.text((person_x - desc_w // 2, person_y + 120), left_desc, fill="#333", font=text_font)

    # 中间：加号
    plus_x = width // 2
    plus_y = 350
    draw.text((plus_x - 30, plus_y - 40), "+", fill="#1a73e8", font=title_font)

    # 右侧
    ai_x = 950
    ai_y = 350
    draw.rectangle(
        [ai_x - 80, ai_y - 80, ai_x + 80, ai_y + 80],
        fill="#2196F3",
        outline="#0D47A1",
        width=4,
    )
    text_bbox = draw.textbbox((0, 0), right_label, font=subtitle_font)
    text_width = text_bbox[2] - text_bbox[0]
    text_height = text_bbox[3] - text_bbox[1]
    draw.text(
        (ai_x - text_width // 2, ai_y - text_height // 2),
        right_label,
        fill="white",
        font=subtitle_font,
    )
    desc_bbox = draw.textbbox((0, 0), right_desc, font=text_font)
    desc_w = desc_bbox[2] - desc_bbox[0]
    draw.text((ai_x - desc_w // 2, ai_y + 120), right_desc, fill="#333", font=text_font)

    # 底部：等号和结果
    draw.text((width // 2 - 30, 550), "=", fill="#1a73e8", font=title_font)

    result_bbox = draw.textbbox((0, 0), result, font=subtitle_font)
    result_width = result_bbox[2] - result_bbox[0]
    draw.text(((width - result_width) // 2, 650), result, fill="#1a73e8", font=subtitle_font)

    img.save(output_path, quality=95)
    print(f"Concept image saved: {output_path}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="生成概念示意图")
    parser.add_argument("--title", default="概念 = A + B", help="图片标题")
    parser.add_argument("--left-label", default="你", help="左侧标签")
    parser.add_argument("--left-desc", default="战略·创意·决策", help="左侧描述")
    parser.add_argument("--right-label", default="AI", help="右侧标签")
    parser.add_argument("--right-desc", default="执行·流程·标准化", help="右侧描述")
    parser.add_argument("--result", default="最终结果", help="底部结果文字")
    parser.add_argument("--output", default="concept.jpg", help="输出文件路径")
    parser.add_argument("--font", default=None, help="字体文件路径")
    args = parser.parse_args()

    create_concept(
        title=args.title,
        left_label=args.left_label,
        left_desc=args.left_desc,
        right_label=args.right_label,
        right_desc=args.right_desc,
        result=args.result,
        output_path=args.output,
        font_file=args.font,
    )
