#!/usr/bin/env python3
"""生成OPC三步流程图"""
from PIL import Image, ImageDraw, ImageFont

def create_opc_flow():
    width = 1200
    height = 800
    
    img = Image.new('RGB', (width, height), 'white')
    draw = ImageDraw.Draw(img)
    
    try:
        title_font = ImageFont.truetype("msyh.ttc", 48)
        step_font = ImageFont.truetype("msyh.ttc", 36)
        text_font = ImageFont.truetype("msyh.ttc", 28)
    except:
        title_font = ImageFont.load_default()
        step_font = ImageFont.load_default()
        text_font = ImageFont.load_default()
    
    # 标题
    title = "OPC三步启动指南"
    title_bbox = draw.textbbox((0, 0), title, font=title_font)
    title_width = title_bbox[2] - title_bbox[0]
    draw.text(((width - title_width) // 2, 40), title, fill='#1a73e8', font=title_font)
    
    # 步骤定义
    steps = [
        {"title": "第一步：注册一人公司", "desc": "在线办理，注册资本1元起"},
        {"title": "第二步：找政策，拿补贴", "desc": "入驻当地OPC社区，享租金、算力优惠"},
        {"title": "第三步：垂直切入，跑通单子", "desc": "从小做起，用AI验证商业模式"},
    ]
    
    start_y = 200
    box_height = 150
    gap_y = 50
    
    # 绘制步骤
    for i, step in enumerate(steps):
        box_y = start_y + i * (box_height + gap_y)
        
        # 步骤框
        draw.rectangle([100, box_y, width - 100, box_y + box_height], fill='#E3F2FD', outline='#90CAF9', width=3)
        
        # 步骤标题
        step_text_bbox = draw.textbbox((0, 0), step["title"], font=step_font)
        step_text_width = step_text_bbox[2] - step_text_bbox[0]
        draw.text((150, box_y + 20), step["title"], fill='#0D47A1', font=step_font)
        
        # 步骤描述
        desc_text_bbox = draw.textbbox((0, 0), step["desc"], font=text_font)
        desc_text_width = desc_text_bbox[2] - desc_text_bbox[0]
        draw.text((150, box_y + 80), step["desc"], fill='#3F51B5', font=text_font)
        
        # 箭头
        if i < len(steps) - 1:
            arrow_start = (width // 2, box_y + box_height + 10)
            arrow_end = (width // 2, box_y + box_height + gap_y - 10)
            draw.line([arrow_start, arrow_end], fill='#1a73e8', width=5)
            draw.polygon([
                (arrow_end[0] - 15, arrow_end[1] - 30),
                (arrow_end[0] + 15, arrow_end[1] - 30),
                (arrow_end[0], arrow_end[1])
            ], fill='#1a73e8')
            
    return img

if __name__ == "__main__":
    img = create_opc_flow()
    img.save("opc_flow.jpg", quality=95)
    print("OPC flow saved: opc_flow.jpg")
