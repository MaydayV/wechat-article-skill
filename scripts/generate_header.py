#!/usr/bin/env python3
"""生成公众号页眉图片"""
from PIL import Image, ImageDraw, ImageFont

def create_header():
    width = 900
    height = 120
    
    img = Image.new('RGB', (width, height), '#1a3a5c')
    draw = ImageDraw.Draw(img)
    
    try:
        title_font = ImageFont.truetype("msyh.ttc", 42)
        sub_font = ImageFont.truetype("msyh.ttc", 24)
        small_font = ImageFont.truetype("msyh.ttc", 18)
    except:
        try:
            title_font = ImageFont.truetype("C:/Windows/Fonts/msyh.ttc", 42)
            sub_font = ImageFont.truetype("C:/Windows/Fonts/msyh.ttc", 24)
            small_font = ImageFont.truetype("C:/Windows/Fonts/msyh.ttc", 18)
        except:
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
    title = "狗哥的胡思乱想"
    title_bbox = draw.textbbox((0, 0), title, font=title_font)
    title_w = title_bbox[2] - title_bbox[0]
    draw.text(((width - title_w) // 2, 38), title, fill='#ffffff', font=title_font)

    # 分割线
    line_y = 90
    draw.rectangle([(width//2 - 20), line_y, (width//2 + 20), line_y + 2], fill='#3daad6')

    # slogan
    slogan = "创业 · AI · 那些没人告诉你的事"
    slogan_bbox = draw.textbbox((0, 0), slogan, font=sub_font)
    slogan_w = slogan_bbox[2] - slogan_bbox[0]
    draw.text(((width - slogan_w) // 2, 96), slogan, fill='#8ab0cc', font=sub_font)

    return img

if __name__ == "__main__":
    img = create_header()
    img.save("header.jpg", quality=95)
    print("Header saved: header.jpg")
