# wechat-article-skill

微信公众号文章创作 Skill —— 一键生成排版精美的公众号文章并推送到草稿箱。

## 功能

- 📝 **文章排版** — 内联 CSS 的 HTML 模板，适配公众号编辑器，手机阅读体验优秀
- 🎨 **封面图生成** — 浅色背景 + 格子纹理 + 思源黑体 Bold，简洁有设计感
- 🚀 **草稿推送** — 自动获取 access_token、上传封面素材、创建草稿，一条命令搞定

## 排版风格

- 16px 正文，2倍行高，两端对齐
- 短句换行，段落留白，阅读节奏舒适
- 蓝色加粗（`#1a73e8`）突出重点观点
- h2 章节标题 + 蓝色下划线分隔
- 浅灰分隔线划分文章段落

## 项目结构

```
wechat-article/
├── SKILL.md                      # Skill 说明（工作流程）
├── references/
│   └── article-style.md          # 排版样式规范（HTML模板+规则）
├── scripts/
│   ├── create_cover.py           # 封面图生成脚本
│   └── publish_draft.py          # 草稿推送脚本
└── assets/
    └── NotoSansCJKsc-Bold.otf    # 思源黑体 Bold（开源免费）
```

## 快速开始

### 1. 安装依赖

```bash
pip3 install Pillow
```

### 2. 配置环境变量

```bash
export WX_APPID="你的AppID"
export WX_APPSECRET="你的AppSecret"
export WX_AUTHOR="作者名"
```

### 3. 生成封面图

```bash
python3 scripts/create_cover.py \
  --title "文章主标题" \
  --subtitle "副标题" \
  --output cover.jpg
```

可选参数：
- `--bg-color "R,G,B"` — 背景色（默认 `235,240,248`）
- `--text-color "R,G,B"` — 标题色（默认 `40,50,75`）
- `--sub-color "R,G,B"` — 副标题色（默认 `90,100,130`）

### 4. 推送到草稿箱

```bash
python3 scripts/publish_draft.py \
  --title "文章标题" \
  --digest "文章摘要" \
  --content-file article.html \
  --cover cover.jpg
```

推送成功后，去公众号后台草稿箱预览确认即可发布。

## 注意事项

- 仅推送到草稿箱，**不会直接发布**
- 封面图尺寸 900×383（2.35:1）
- 需要在公众号后台将服务器 IP 加入白名单
- 字体使用[思源黑体](https://github.com/googlefonts/noto-cjk)（SIL Open Font License），可自由商用

## License

MIT
