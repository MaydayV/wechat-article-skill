#!/usr/bin/env python3
"""生成城市政策对比表图片"""
from PIL import Image, ImageDraw, ImageFont
import os

def create_policy_table():
    # 图片尺寸
    width = 1200
    height = 1400
    
    # 创建白色背景
    img = Image.new('RGB', (width, height), 'white')
    draw = ImageDraw.Draw(img)
    
    # 尝试使用系统字体
    try:
        title_font = ImageFont.truetype("msyh.ttc", 48)  # 微软雅黑
        header_font = ImageFont.truetype("msyh.ttc", 32)
        content_font = ImageFont.truetype("msyh.ttc", 28)
    except:
        title_font = ImageFont.load_default()
        header_font = ImageFont.load_default()
        content_font = ImageFont.load_default()
    
    # 标题
    title = "全国OPC政策对比"
    title_bbox = draw.textbbox((0, 0), title, font=title_font)
    title_width = title_bbox[2] - title_bbox[0]
    draw.text(((width - title_width) // 2, 40), title, fill='#1a73e8', font=title_font)
    
    # 表格数据
    data = [
        ("城市", "核心政策", "补贴力度"),
        ("深圳", "训力券+模型券+产业基金", "最高1000万"),
        ("苏州", "政策性股权投资", "最高2000万"),
        ("上海", "办公免租+公寓免费", "10万启动金"),
        ("武汉", "算力费用补贴50%", "每年20万"),
        ("北京", "租金减免+人才公寓", "3年免租"),
        ("青岛", "AI项目资助+算力补贴", "最高100万"),
    ]
    
    # 表格位置
    start_y = 150
    row_height = 180
    col_widths = [200, 600, 300]
    
    # 绘制表头
    x = 50
    for i, header in enumerate(data[0]):
        # 表头背景
        draw.rectangle(
            [x, start_y, x + col_widths[i], start_y + row_height],
            fill='#1a73e8',
            outline='#0d47a1',
            width=2
        )
        # 表头文字
        text_bbox = draw.textbbox((0, 0), header, font=header_font)
        text_width = text_bbox[2] - text_bbox[0]
        text_height = text_bbox[3] - text_bbox[1]
        draw.text(
            (x + (col_widths[i] - text_width) // 2, start_y + (row_height - text_height) // 2),
            header,
            fill='white',
            font=header_font
        )
        x += col_widths[i]
    
    # 绘制数据行
    for row_idx, row in enumerate(data[1:], 1):
        x = 50
        y = start_y + row_idx * row_height
        
        # 交替行颜色
        bg_color = '#f5f5f5' if row_idx % 2 == 0 else 'white'
        
        for col_idx, cell in enumerate(row):
            # 单元格背景
            draw.rectangle(
                [x, y, x + col_widths[col_idx], y + row_height],
                fill=bg_color,
                outline='#cccccc',
                width=1
            )
            
            # 单元格文字（支持换行）
            lines = []
            if len(cell) > 12 and col_idx == 1:  # 中间列需要换行
                words = cell.split('+')
                for word in words:
                    lines.append(word)
            else:
                lines = [cell]
            
            # 计算总文字高度
            total_height = len(lines) * 35
            current_y = y + (row_height - total_height) // 2
            
            for line in lines:
                text_bbox = draw.textbbox((0, 0), line, font=content_font)
                text_width = text_bbox[2] - text_bbox[0]
                draw.text(
                    (x + (col_widths[col_idx] - text_width) // 2, current_y),
                    line,
                    fill='#333333',
                    font=content_font
                )
                current_y += 35
            
            x += col_widths[col_idx]
    
    # 底部说明
    note = "数据来源：各地政府官方政策文件（2025-2026）"
    note_bbox = draw.textbbox((0, 0), note, font=content_font)
    note_width = note_bbox[2] - note_bbox[0]
    draw.text(
        ((width - note_width) // 2, height - 80),
        note,
        fill='#666666',
        font=content_font
    )
    
    return img

if __name__ == "__main__":
    img = create_policy_table()
    output_path = "policy_table.jpg"
    img.save(output_path, quality=95)
    print(f"Policy table saved: {output_path}")
