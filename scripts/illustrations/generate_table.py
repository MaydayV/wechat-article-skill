#!/usr/bin/env python3
"""
生成城市政策对比表图片（通用版）。

用法:
  python3 generate_table.py --title "XX政策对比" \
    --headers "列1,列2,列3" \
    --rows "值1a,值1b,值1c;值2a,值2b,值2c" \
    --note "数据来源说明" \
    --output table.jpg
"""
import argparse
import os
import sys
from typing import List, Optional

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import font_utils

from PIL import Image, ImageDraw, ImageFont


def create_policy_table(
    title: str = "数据对比表",
    headers: List[str] = None,
    rows: List[str] = None,
    note: str = "数据来源说明",
    output_path: str = "table.jpg",
    font_file: Optional[str] = None,
):
    if headers is None:
        headers = ["类别", "项目", "结果"]
    if rows is None:
        rows = ["A,X,100", "B,Y,200", "C,Z,300"]

    # 图片尺寸
    width = 1200
    row_height_base = 100
    
    # 动态计算高度
    num_rows = len(rows)
    # 预估内容高度，每行文本大概高度35
    total_content_height = 0
    for row_str in rows:
        cells = row_str.split(',')
        max_lines_in_row = 1
        for cell in cells:
            # 简单估算，每 12 个字符换一行
            max_lines_in_row = max(max_lines_in_row, (len(cell) + 11) // 12)
        total_content_height += max_lines_in_row * 35 + 20 # 文本高度 + 内边距

    # 表头 + 数据 + 标题 + 底部说明的预留空间
    height = 150 + row_height_base + total_content_height + 150 
    if height < 800: height = 800

    # 创建白色背景
    img = Image.new("RGB", (width, height), "white")
    draw = ImageDraw.Draw(img)

    # 尝试使用系统字体
    try:
        actual_font_path = font_utils.find_chinese_font(preferred=font_file)
        title_font = ImageFont.truetype(actual_font_path, 48)
        header_font = ImageFont.truetype(actual_font_path, 32)
        content_font = ImageFont.truetype(actual_font_path, 28)
    except FileNotFoundError:
        title_font = ImageFont.load_default()
        header_font = ImageFont.load_default()
        content_font = ImageFont.load_default()

    # 标题
    title_bbox = draw.textbbox((0, 0), title, font=title_font)
    title_width = title_bbox[2] - title_bbox[0]
    draw.text(((width - title_width) // 2, 40), title, fill="#1a73e8", font=title_font)

    # 表格位置
    start_y = 150
    # 动态计算列宽，平均分配
    num_cols = len(headers)
    col_widths = [ (width - 100) // num_cols for _ in range(num_cols) ]
    
    # 调整第一列和最后一列的宽度，如果需要
    # if num_cols > 2:
    #     col_widths[0] = 200 # 例如，固定第一列宽度
    #     col_widths[-1] = 200 # 例如，固定最后一列宽度
    #     remaining_width = width - 100 - col_widths[0] - col_widths[-1]
    #     if num_cols > 2:
    #         for i in range(1, num_cols - 1):
    #             col_widths[i] = remaining_width // (num_cols - 2)

    # 绘制表头
    current_x = 50
    for i, header in enumerate(headers):
        # 表头背景
        draw.rectangle(
            [current_x, start_y, current_x + col_widths[i], start_y + row_height_base],
            fill="#1a73e8",
            outline="#0d47a1",
            width=2,
        )
        # 表头文字
        text_bbox = draw.textbbox((0, 0), header, font=header_font)
        text_width = text_bbox[2] - text_bbox[0]
        draw.text(
            (current_x + (col_widths[i] - text_width) // 2, start_y + (row_height_base - (text_bbox[3]-text_bbox[1])) // 2),
            header,
            fill="white",
            font=header_font,
        )
        current_x += col_widths[i]

    # 绘制数据行
    current_y = start_y + row_height_base
    for row_idx, row_str in enumerate(rows):
        cells = row_str.split(",")
        current_x = 50

        # 计算当前行的实际高度
        max_cell_lines = 1
        for cell_content in cells:
            # 估算每列最多多少行
            max_cell_lines = max(max_cell_lines, (len(cell_content) * 28 // (col_widths[0]-20) + 1)) # 假设每行大约能放xx个字符，28是字号，减20是左右边距

        actual_row_height = max_cell_lines * 35 # 35是行高估算

        # 交替行颜色
        bg_color = "#f5f5f5" if (row_idx + 1) % 2 == 0 else "white" # 表头不算第一行

        for col_idx, cell_content in enumerate(cells):
            # 单元格背景
            draw.rectangle(
                [current_x, current_y, current_x + col_widths[col_idx], current_y + actual_row_height],
                fill=bg_color,
                outline="#cccccc",
                width=1,
            )

            # 单元格文字（支持换行）
            lines = []
            current_line = ""
            words = list(cell_content) # 按字符分割
            
            for word in words:
                test_line = current_line + word
                test_bbox = draw.textbbox((0,0), test_line, font=content_font)
                test_width = test_bbox[2] - test_bbox[0]
                if test_width < col_widths[col_idx] - 20: # 留出左右边距
                    current_line += word
                else:
                    lines.append(current_line)
                    current_line = word
            lines.append(current_line) # 添加最后一行


            # 计算总文字高度
            total_text_height_in_cell = len(lines) * 35 # 35是行高
            text_start_y = current_y + (actual_row_height - total_text_height_in_cell) // 2

            for line in lines:
                text_bbox = draw.textbbox((0, 0), line, font=content_font)
                text_width = text_bbox[2] - text_bbox[0]
                draw.text(
                    (current_x + (col_widths[col_idx] - text_width) // 2, text_start_y),
                    line,
                    fill="#333333",
                    font=content_font,
                )
                text_start_y += 35 # 每行间隔

            current_x += col_widths[col_idx]
        current_y += actual_row_height


    # 底部说明
    note_bbox = draw.textbbox((0, 0), note, font=content_font)
    note_width = note_bbox[2] - note_bbox[0]
    draw.text(
        ((width - note_width) // 2, height - 80),
        note,
        fill="#666666",
        font=content_font,
    )

    img.save(output_path, quality=95)
    print(f"Policy table saved: {output_path}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="生成通用数据对比表图片")
    parser.add_argument("--title", default="数据对比表", help="表格标题")
    parser.add_argument(
        "--headers",
        type=lambda s: s.split(","),
        default=["类别", "项目", "结果"],
        help='表头，逗号分隔。例如: "城市,核心政策,补贴力度"',
    )
    parser.add_argument(
        "--rows",
        type=lambda s: s.split(";"),
        default=["A,X,100", "B,Y,200", "C,Z,300"],
        help='数据行，分号分隔行，逗号分隔列。例如: "深圳,训力券+模型券+产业基金,最高1000万;上海,办公免租+公寓免费,10万启动金"',
    )
    parser.add_argument("--note", default="数据来源说明", help="底部说明文字")
    parser.add_argument("--output", default="table.jpg", help="输出文件路径")
    parser.add_argument("--font", default=None, help="字体文件路径")
    args = parser.parse_args()

    create_policy_table(
        title=args.title,
        headers=args.headers,
        rows=args.rows,
        note=args.note,
        output_path=args.output,
        font_file=args.font,
    )