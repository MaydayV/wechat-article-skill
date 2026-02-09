---
name: wechat-article
description: Create, format, and publish WeChat Official Account (微信公众号) articles with consistent styling and cover images. Use when user wants to write, format, or publish a 公众号 article, generate a cover image for 公众号, or push content to WeChat draft box.
---

# 微信公众号文章创作

## 配置

所有配置存放在工作区的 `wechat-article.config.json` 文件中。

### 首次使用

如果 `wechat-article.config.json` 不存在，进入**初始化配置**流程：

通过对话逐步询问用户以下信息，收集完成后写入配置文件：

```json
{
  "appid": "公众号 AppID",
  "appsecret": "公众号 AppSecret",
  "author": "默认作者名",
  "writing": {
    "perspective": "第一人称",
    "tone": "口语化，像跟朋友聊天分享观点",
    "length": "1500-2500字",
    "direction": "科技/AI/产品思考",
    "keywords_style": "短句为主，一行不超过30字"
  }
}
```

引导话术示例：

> 首次使用公众号文章功能，我需要了解几个信息来帮你配置：
> 1. 公众号的 AppID 和 AppSecret 是什么？（需要在公众号后台将服务器IP加白名单）
> 2. 文章的默认作者名？
> 3. 你的写作风格偏好：
>    - 用什么视角？（第一人称 / 第三人称 / 旁观者）
>    - 什么语气？（口语化聊天 / 正式专业 / 幽默风趣 / 其他）
>    - 文章通常多长？（1000字左右 / 1500-2500字 / 3000字以上）
>    - 主要写什么方向？（科技/生活/商业/其他）

用户可以一次性回答，也可以逐条回答。收集完后写入 `wechat-article.config.json`。

### 后续使用

配置文件存在时，直接读取，用户只需提供**文章主题**即可，例如：

> "帮我写一篇公众号文章，聊聊AI让创新变简单了"

agent 根据配置中的写作风格自动完成：写内容 → 排版 → 生成封面图 → 推送草稿。

### 修改配置

用户随时可以说"修改公众号配置"或"更新写作风格"，agent 读取现有配置，询问要改哪项，更新后写回文件。

## 工作流程

### 1. 读取配置

读取 `wechat-article.config.json`，获取凭证和写作风格。不存在则进入初始化流程。

### 2. 创作文章

根据用户主题 + 配置中的写作风格生成文章：

- **视角**：按 `writing.perspective` 设定
- **语气**：按 `writing.tone` 设定
- **长度**：按 `writing.length` 控制
- **方向**：按 `writing.direction` 参考

### 3. 排版为 HTML

按 [references/article-style.md](references/article-style.md) 的排版规范格式化。

核心要素：
- `<p>` 标签：`font-size:16px; line-height:2; color:#333; margin:15px 0; text-align:justify`
- 短句用 `<br />` 换行
- 重点句用 `<strong style="color: #1a73e8;">` 蓝色加粗（每篇 3-6 处）
- 段落间用 `<hr style="border:none; border-top:1px solid #eee; margin:30px 0;" />` 分隔
- 章节标题用 `<h2>` + 蓝色下划线（见 references/article-style.md）
- 外层 `<section>` 带 font-family 和 padding

### 4. 生成封面图

运行封面图脚本（依赖 Pillow，需先 `pip3 install Pillow -q`）：

```bash
python3 scripts/create_cover.py \
  --title "主标题" \
  --subtitle "副标题" \
  --output cover.jpg
```

可选参数：
- `--bg-color "R,G,B"` — 背景色（默认 `235,240,248` 浅灰蓝）
- `--text-color "R,G,B"` — 标题色（默认 `40,50,75` 深蓝灰）
- `--sub-color "R,G,B"` — 副标题色（默认 `90,100,130`）

封面图特征：浅色背景 + 格子纹理 + 对角线装饰 + 思源黑体 Bold 文字。

字体文件：`assets/NotoSansCJKsc-Bold.otf`（思源黑体，开源免费无版权）。

### 5. 推送到草稿箱

运行发布脚本：

```bash
python3 scripts/publish_draft.py \
  --title "文章标题" \
  --author "作者名" \
  --digest "文章摘要（120字以内）" \
  --content-file article.html \
  --cover cover.jpg \
  --appid <从配置读取> \
  --appsecret <从配置读取>
```

脚本也支持环境变量 `WX_APPID`、`WX_APPSECRET`、`WX_AUTHOR`。

脚本会自动：获取 access_token → 上传封面图为永久素材 → 创建草稿。

### 注意事项

- 仅推送到草稿箱，**不会直接发布**
- 推送后提醒用户去公众号后台预览确认
- 封面图尺寸 900×383（2.35:1 比例）
- **不要在 skill 文件中存放敏感信息**，凭证保存在用户本地的 `wechat-article.config.json` 中
