---
name: wechat-article
description: Create, format, and publish WeChat Official Account (微信公众号) articles with consistent styling and cover images. Use when user wants to write, format, or publish a 公众号 article, generate a cover image for 公众号, or push content to WeChat draft box.
---

# 微信公众号文章创作

## 配置

公众号的 AppID、AppSecret、作者等信息存放在 `TOOLS.md` 中，不要硬编码在 skill 内。

使用前确认 `TOOLS.md` 中包含以下字段：
- AppID
- AppSecret
- 默认作者

## 工作流程

### 1. 写文章内容

根据用户主题创作文章，写作风格：
- **第一视角**，像跟朋友聊天分享观点
- 短句为主，一行不超过 30 字左右
- 口语化，不要书面腔

### 2. 排版为 HTML

按 [references/article-style.md](references/article-style.md) 的排版规范格式化为内联 CSS 的 HTML。

核心要素：
- `<p>` 标签：`font-size:16px; line-height:2; color:#333; margin:15px 0; text-align:justify`
- 短句用 `<br />` 换行
- 重点句用 `<strong style="color: #1a73e8;">` 蓝色加粗（每篇 3-6 处）
- 段落间用 `<hr style="border:none; border-top:1px solid #eee; margin:30px 0;" />` 分隔
- 外层 `<section>` 带 font-family 和 padding
- 章节标题用 `<h2>` + 蓝色下划线（见 references/article-style.md）

### 3. 生成封面图

运行封面图脚本（依赖 Pillow，需先 `pip3 install Pillow -q`）：

```bash
python3 scripts/create_cover.py \
  --title "主标题" \
  --subtitle "副标题" \
  --output /path/to/cover.jpg
```

可选参数：
- `--bg-color "R,G,B"` — 背景色（默认 `235,240,248` 浅灰蓝）
- `--text-color "R,G,B"` — 标题色（默认 `40,50,75` 深蓝灰）
- `--sub-color "R,G,B"` — 副标题色（默认 `90,100,130`）

封面图特征：浅色背景 + 格子纹理 + 对角线装饰 + 思源黑体 Bold 文字。

字体文件：`assets/NotoSansCJKsc-Bold.otf`（思源黑体，开源免费无版权）。

### 4. 推送到草稿箱

运行发布脚本，通过环境变量或参数传入 AppID 和 AppSecret：

```bash
python3 scripts/publish_draft.py \
  --title "文章标题" \
  --author "作者名" \
  --digest "文章摘要（120字以内）" \
  --content-file article.html \
  --cover cover.jpg \
  --appid <从TOOLS.md读取> \
  --appsecret <从TOOLS.md读取>
```

也可通过环境变量 `WX_APPID` 和 `WX_APPSECRET` 传入。

脚本会自动：获取 access_token → 上传封面图为永久素材 → 创建草稿。

### 注意事项

- 仅推送到草稿箱，**不会直接发布**
- 推送后提醒用户去公众号后台预览确认
- 封面图尺寸 900×383（2.35:1 比例）
- **不要在 skill 文件中存放 AppID、AppSecret 等敏感信息**
