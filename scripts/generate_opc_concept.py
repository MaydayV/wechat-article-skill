#!/usr/bin/env python3
"""生成OPC概念示意图"""
from PIL import Image, ImageDraw, ImageFont

def create_opc_concept():
    width = 1200
    height = 800
    
    img = Image.new('RGB', (width, height), 'white')
    draw = ImageDraw.Draw(img)
    
    try:
        title_font = ImageFont.truetype("msyh.ttc", 56)
        subtitle_font = ImageFont.truetype("msyh.ttc", 36)
        text_font = ImageFont.truetype("msyh.ttc", 32)
    except:
        title_font = ImageFont.load_default()
        subtitle_font = ImageFont.load_default()
        text_font = ImageFont.load_default()
    
    # 背景渐变效果（简化版）
    for y in range(height):
        color_value = int(245 + (255 - 245) * (y / height))
        draw.line([(0, y), (width, y)], fill=(color_value, color_value, 255))
    
    # 标题
    title = "OPC = 个人 + AI"
    title_bbox = draw.textbbox((0, 0), title, font=title_font)
    title_width = title_bbox[2] - title_bbox[0]
    draw.text(((width - title_width) // 2, 80), title, fill='#1a73e8', font=title_font)
    
    # 左侧：个人
    person_x = 250
    person_y = 350
    draw.ellipse([person_x-80, person_y-80, person_x+80, person_y+80], fill='#4CAF50', outline='#2E7D32', width=4)
    person_text = "你"
    text_bbox = draw.textbbox((0, 0), person_text, font=subtitle_font)
    text_width = text_bbox[2] - text_bbox[0]
    text_height = text_bbox[3] - text_bbox[1]
    draw.text((person_x - text_width//2, person_y - text_height//2), person_text, fill='white', font=subtitle_font)
    
    draw.text((person_x - 100, person_y + 120), "战略·创意·决策", fill='#333', font=text_font)
    
    # 中间：加号
    plus_x = width // 2
    plus_y = 350
    draw.text((plus_x - 30, plus_y - 40), "+", fill='#1a73e8', font=title_font)
    
    # 右侧：AI
    ai_x = 950
    ai_y = 350
    draw.rectangle([ai_x-80, ai_y-80, ai_x+80, ai_y+80], fill='#2196F3', outline='#0D47A1', width=4)
    ai_text = "AI"
    text_bbox = draw.textbbox((0, 0), ai_text, font=subtitle_font)
    text_width = text_bbox[2] - text_bbox[0]
    text_height = text_bbox[3] - text_bbox[1]
    draw.text((ai_x - text_width//2, ai_y - text_height//2), ai_text, fill='white', font=subtitle_font)
    
    draw.text((ai_x - 100, ai_y + 120), "执行·流程·标准化", fill='#333', font=text_font)
    
    # 底部：等号和结果
    draw.text((width//2 - 30, 550), "=", fill='#1a73e8', font=title_font)
    
    result = "一家公司的全链路能力"
    result_bbox = draw.textbbox((0, 0), result, font=subtitle_font)
    result_width = result_bbox[2] - result_bbox[0]
    draw.text(((width - result_width) // 2, 650), result, fill='#1a73e8', font=subtitle_font)
    
    return img

if __name__ == "__main__":
    img = create_opc_concept()
    img.save("opc_concept.jpg", quality=95)
    print("OPC concept saved: opc_concept.jpg")
