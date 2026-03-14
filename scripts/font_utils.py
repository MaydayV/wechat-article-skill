#!/usr/bin/env python3
"""
跨平台中文字体查找工具。

所有推荐字体均为免费商用：
- Noto Sans CJK SC（思源黑体，SIL OFL）— skill 自带
- PingFang SC（苹方）— macOS 系统自带
- Source Han Sans（思源黑体 Adobe 版，SIL OFL）
- WenQuanYi Micro Hei（文泉驿微米黑，GPL+FE）
"""
import os
import sys
from typing import Optional

# 按优先级排列的字体候选列表
# 格式: (名称, 路径列表)
FONT_CANDIDATES = [
    # macOS 系统字体
    ("PingFang SC Bold", [
        "/System/Library/Fonts/PingFang.ttc",
        "/System/Library/Fonts/Supplemental/PingFang.ttc",
    ]),
    ("Hiragino Sans GB", [
        "/System/Library/Fonts/Supplemental/Hiragino Sans GB.ttc",
        "/Library/Fonts/Hiragino Sans GB.ttc",
    ]),
    # Windows 系统字体
    ("Microsoft YaHei", [
        "C:/Windows/Fonts/msyh.ttc",
        "C:/Windows/Fonts/msyhbd.ttc",
    ]),
    ("SimHei", [
        "C:/Windows/Fonts/simhei.ttf",
    ]),
    # Linux 字体
    ("Noto Sans CJK SC", [
        "/usr/share/fonts/opentype/noto/NotoSansCJK-Bold.ttc",
        "/usr/share/fonts/noto-cjk/NotoSansCJKsc-Bold.otf",
        "/usr/share/fonts/google-noto-cjk/NotoSansCJKsc-Bold.otf",
        "/usr/share/fonts/OTF/NotoSansCJKsc-Bold.otf",
    ]),
    ("WenQuanYi Micro Hei", [
        "/usr/share/fonts/wenquanyi/wqy-microhei/wqy-microhei.ttc",
        "/usr/share/fonts/truetype/wqy/wqy-microhei.ttc",
    ]),
    ("Source Han Sans", [
        "/usr/share/fonts/adobe-source-han-sans/SourceHanSansSC-Bold.otf",
        "/usr/share/fonts/opentype/source-han-sans/SourceHanSansSC-Bold.otf",
    ]),
]


def _skill_bundled_font() -> Optional[str]:
    """返回 skill 自带的 NotoSansCJKsc-Bold.otf 路径（如果存在）。"""
    # 从 scripts/ 向上找 assets/
    script_dir = os.path.dirname(os.path.abspath(__file__))
    skill_dir = os.path.dirname(script_dir)
    bundled = os.path.join(skill_dir, "assets", "NotoSansCJKsc-Bold.otf")
    if os.path.isfile(bundled):
        return bundled
    return None


def find_chinese_font(preferred: Optional[str] = None) -> str:
    """
    查找可用的中文字体文件路径。

    优先级：
    1. 用户指定的 preferred 路径
    2. skill 自带字体 assets/NotoSansCJKsc-Bold.otf
    3. 系统字体（macOS → Windows → Linux）
    4. 抛出 FileNotFoundError

    Args:
        preferred: 用户指定的字体文件路径

    Returns:
        可用的字体文件绝对路径

    Raises:
        FileNotFoundError: 找不到任何可用的中文字体
    """
    # 1. 用户指定
    if preferred and os.path.isfile(preferred):
        return os.path.abspath(preferred)

    # 2. skill 自带
    bundled = _skill_bundled_font()
    if bundled:
        return bundled

    # 3. 系统字体
    for name, paths in FONT_CANDIDATES:
        for p in paths:
            if os.path.isfile(p):
                return p

    raise FileNotFoundError(
        "找不到可用的中文字体。请安装 Noto Sans CJK SC 或将字体文件放到 assets/ 目录。\n"
        "下载地址: https://github.com/googlefonts/noto-cjk/releases"
    )


def list_available_fonts() -> list:
    """列出当前系统上所有可用的中文字体。"""
    available = []

    bundled = _skill_bundled_font()
    if bundled:
        available.append(("Noto Sans CJK SC (bundled)", bundled))

    for name, paths in FONT_CANDIDATES:
        for p in paths:
            if os.path.isfile(p):
                available.append((name, p))
                break

    return available


if __name__ == "__main__":
    print("可用中文字体：")
    fonts = list_available_fonts()
    if not fonts:
        print("  (无)")
    else:
        for name, path in fonts:
            print(f"  - {name}: {path}")

    print()
    try:
        best = find_chinese_font()
        print(f"推荐字体: {best}")
    except FileNotFoundError as e:
        print(f"错误: {e}", file=sys.stderr)
