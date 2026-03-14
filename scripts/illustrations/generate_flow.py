#!/usr/bin/env python3
"""
生成流程图。

用法:
  python3 generate_flow.py --title "三步流程图" \
    --steps "第一步:描述1;第二步:描述2;第三步:描述3" \
    --output flow.jpg
"""
import argparse
import os
import sys
from typing import List, Optional

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import font_utils

from PIL import Image, ImageDraw, ImageFont


def create_flow(
    title: str = "三步流程图",
    steps_data: List[str] = None, # 格式: "标题:描述"
    output_path: str = "flow.jpg",
    font_file: Optional[str] = None,
):
    if steps_data is None:
        steps_data = [
            "第一步:详细描述第一步的操作或目标",
            "第二步:详细描述第二步的操作或目标",
            "第三步:详细描述第三步的操作或目标",
        ]
    
    steps = []
    for s_data in steps_data:
        parts = s_data.split(":", 1)
        if len(parts) == 2:
            steps.append({"title": parts[0].strip(), "desc": parts[1].strip()})
        else:
            steps.append({"title": s_data.strip(), "desc": ""})


    width = 1200
    height = 200 + len(steps) * 200 # 根据步骤数量调整高度
    if height < 800: height = 800 # 最小高度

    img = Image.new("RGB", (width, height), "white")
    draw = ImageDraw.Draw(img)

    try:
        actual_font_path = font_utils.find_chinese_font(preferred=font_file)
        title_font = ImageFont.truetype(actual_font_path, 48)
        step_font = ImageFont.truetype(actual_font_path, 36)
        text_font = ImageFont.truetype(actual_font_path, 28)
    except FileNotFoundError:
        title_font = ImageFont.load_default()
        step_font = ImageFont.load_default()
        text_font = ImageFont.load_default()

    # 标题
    title_bbox = draw.textbbox((0, 0), title, font=title_font)
    title_width = title_bbox[2] - title_bbox[0]
    draw.text(((width - title_width) // 2, 40), title, fill="#1a73e8", font=title_font)

    box_height = 120
    gap_y = 50
    start_y = 150 # 初始Y坐标

    # 绘制步骤
    for i, step in enumerate(steps):
        box_y = start_y + i * (box_height + gap_y)

        # 步骤框
        draw.rounded_rectangle([100, box_y, width - 100, box_y + box_height], radius=15, fill="#E3F2FD", outline="#90CAF9", width=3)

        # 步骤标题
        step_text_bbox = draw.textbbox((0, 0), step["title"], font=step_font)
        step_text_width = step_text_bbox[2] - step_text_bbox[0]
        draw.text((150, box_y + 20), step["title"], fill="#0D47A1", font=step_font)

        # 步骤描述
        if step["desc"]:
            desc_text_bbox = draw.textbbox((0, 0), step["desc"], font=text_font)
            # desc_text_width = desc_text_bbox[2] - desc_text_bbox[0]
            draw.text((150, box_y + 65), step["desc"], fill="#3F51B5", font=text_font)

        # 箭头
        if i < len(steps) - 1:
            arrow_start = (width // 2, box_y + box_height + 10)
            arrow_end = (width // 2, box_y + box_height + gap_y - 10)
            draw.line([arrow_start, arrow_end], fill="#1a73e8", width=5)
            draw.polygon(
                [
                    (arrow_end[0] - 15, arrow_end[1] - 30),
                    (arrow_end[0] + 15, arrow_end[1] - 30),
                    (arrow_end[0], arrow_end[1]),
                ],
                fill="#1a73e8",
            )

    img.save(output_path, quality=95)
    print(f"Flow image saved: {output_path}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="生成流程图")
    parser.add_argument("--title", default="三步流程图", help="流程图标题")
    parser.add_argument(
        "--steps",
        nargs="+",
        default=None,
        help='步骤列表，格式为 "标题:描述"。例如: "注册公司:在线办理;找政策:入驻社区;垂直切入:用AI验证"',
    )
    parser.add_argument("--output", default="flow.jpg", help="输出文件路径")
    parser.add_argument("--font", default=None, help="字体文件路径")
    args = parser.parse_args()

    create_flow(
        title=args.title,
        steps_data=args.steps,
        output_path=args.output,
        font_file=args.font,
    )
