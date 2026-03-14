# wechat-article-skill

微信公众号文章创作 Skill —— 从主题到草稿箱，一句话搞定。

> 面向 OpenClaw 的微信公众号创作与草稿发布能力。支持：文章生成、公众号友好排版、封面风格化生成、发布前图文预览确认、推送草稿箱。

---

## 功能

- 🧬 **写作风格DNA**：基于你的参考文章自动提取写作风格，每个人的输出天然不同
- ✍️ **AI 文章创作**：只需一句主题，按你的风格DNA生成完整文章
- 📝 **公众号排版**：内联 CSS HTML 模板，适配微信编辑器，支持多种排版风格
- 🎨 **封面风格系统**：PIL 方案（4 种风格 × 6 套配色）+ HTML 模板方案（Playwright 截图）
- 🖼️ **正文配图生成**：概念图、流程图、数据表格等配图脚本
- 📖 **公众号文章读取**：自动抓取微信公众号文章内容（Camoufox + 多层降级）
- 👀 **发布前预览确认**：先看正文预览 + 封面预览，再决定是否发布
- 🚀 **草稿推送**：自动上传封面并创建草稿（默认不直接群发）
- 🔄 **持续进化**：每次创作交互自动学习你的偏好，风格DNA越用越准

---

## 快速开始（OpenClaw）

### 1) 放置 Skill 目录

将本仓库放到 OpenClaw skills 目录：

```bash
~/.openclaw/skills/wechat-article-skill
```

### 2) 在对话中触发

示例：

- `帮我写一篇公众号文章，主题是 XXX`
- `把这篇文章生成封面并推送到草稿箱`
- `修改公众号配置`

### 3) 首次配置（自动引导）

首次触发会询问并保存到 `wechat-article.config.json`：

1. 公众号 `AppID` / `AppSecret`
2. 公众号名称 (`account_name`) 和 Slogan (`slogan`)
3. 默认作者
4. 写作风格（视角、语气、长度、方向）
5. 排版风格（`default` 或 `gougestyle`）
6. 评论开关
7. 封面策略（HTML 模板或 PIL 方案）
8. **写作风格DNA**：提供3-5篇你喜欢的公众号文章链接，系统自动分析并生成你的专属写作风格

---

## 封面风格系统

### HTML 模板方案（推荐）

使用 Playwright 渲染 HTML 模板并截图，效果最好。

可用模板：
- `akai-cover`（阿凯封面模板）：极简白底、左侧渐变竖线、大标题居左
- `gouge-cover`（狗哥封面模板）：深色科技风、网格背景、光晕装饰

### PIL 方案

使用 Pillow 库生成封面图，无需浏览器环境。

风格（Style）：
1. `minimal-grid`（极简网格）
2. `card-editorial`（编辑卡片）
3. `diagonal-motion`（斜切动势）
4. `soft-gradient`（柔和渐变）

配色（Palette）：
1. `blue-tech`（科技蓝）
2. `purple-insight`（洞察紫）
3. `green-growth`（增长绿）
4. `orange-energy`（活力橙）
5. `rose-story`（故事玫红）
6. `slate-pro`（专业灰）

---

## 排版风格

- `default`：标准排版（16px, 2倍行高, 两端对齐）
- `gougestyle`：狗哥排版（15px, 1.75倍行高, 左对齐, 微信兼容优化）

详见 `references/styles/` 目录。

---

## 写作风格DNA

每个用户的写作风格来自自己的参考文章，而不是公共模板。

### 工作原理

1. 你提供3-5篇喜欢的公众号文章链接
2. 系统自动抓取并分析文章风格（句式、节奏、金句结构、开头结尾偏好等）
3. 生成你的专属 `style-dna.md` 风格档案
4. 后续每篇文章都基于这个档案生成
5. 每次创作交互中，系统根据你的反馈持续进化DNA

### 为什么不用公共模板？

公共模板用的人越多，大家的内容越像。风格DNA确保每个人的输出天然不同，因为每个人的参考文章不同。

### DNA 进化

- 你说"这个开头太平了" → DNA 记录你不喜欢平铺直叙
- 你选了标题B而不是A → DNA 记录你的标题偏好
- 你手动改了某段 → DNA 对比改前改后，提取偏好变化
- 越用越懂你，越用越像你

---

## 正文配图

`scripts/illustrations/` 目录下提供配图生成脚本：

- `generate_concept.py`：概念示意图
- `generate_flow.py`：流程图
- `generate_table.py`：数据表格图
- `generate_header.py`：页眉图片

所有脚本支持命令行参数，跨平台字体自动查找。

---

## 项目结构

```text
wechat-article-skill/
├── SKILL.md
├── README.md
├── assets/
│   ├── NotoSansCJKsc-Bold.otf
│   └── cover-style-palette-preview-grid.jpg
├── references/
│   ├── article-style.md              (排版风格索引)
│   ├── style-dna-template.md         (风格DNA空白模板)
│   ├── style-dna.md                  (用户风格DNA，系统生成)
│   ├── my-articles/                  (用户参考文章)
│   │   └── README.md
│   └── styles/
│       ├── default.md                (默认排版风格)
│       └── gougestyle.md             (狗哥排版风格)
├── templates/
│   └── covers/
│       ├── akai-cover.html           (阿凯封面模板)
│       └── gouge-cover.html          (狗哥封面模板)
└── scripts/
    ├── font_utils.py                 (跨平台字体工具)
    ├── create_cover.py               (封面生成脚本)
    ├── create_cover_preview_grid.py
    ├── publish_draft.py              (草稿发布脚本)
    └── illustrations/
        ├── generate_concept.py       (概念示意图生成)
        ├── generate_flow.py          (流程图生成)
        ├── generate_header.py        (页眉图片生成)
        └── generate_table.py         (数据表格图生成)
```

---

## 独立脚本使用（不依赖 OpenClaw）

### 安装依赖

```bash
pip3 install Pillow jinja2 playwright
playwright install chromium
```

### 生成封面（PIL 方案）

```bash
python3 scripts/create_cover.py \
  --title "文章主标题" \
  --subtitle "副标题" \
  --style minimal-grid \
  --palette auto \
  --rotate sequential \
  --output cover.jpg
```

### 生成封面（HTML 模板方案）

```bash
python3 scripts/create_cover.py \
  --html-template templates/covers/akai-cover.html \
  --title "文章主标题" \
  --subtitle "副标题" \
  --account-name "你的公众号名称" \
  --slogan "你的 Slogan" \
  --tag "AI · 2026" \
  --output cover.jpg
```

### 生成配图

```bash
# 概念图
python3 scripts/illustrations/generate_concept.py \
  --title "核心概念" --left-label "你" --right-label "AI" --output concept.jpg

# 流程图
python3 scripts/illustrations/generate_flow.py \
  --title "三步流程" --steps "第一步:描述1" "第二步:描述2" "第三步:描述3" --output flow.jpg

# 数据表格
python3 scripts/illustrations/generate_table.py \
  --title "对比表" --headers "城市,政策,补贴" --rows "深圳,训力券,最高1000万;上海,免租,10万" --output table.jpg
```

### 推送草稿

```bash
python3 scripts/publish_draft.py \
  --title "文章标题" \
  --author "作者名" \
  --digest "文章摘要" \
  --content-file article.html \
  --cover cover.jpg \
  --appid "你的AppID" \
  --appsecret "你的AppSecret" \
  --content-img concept=concept.jpg \
  --content-img flow=flow.jpg
```

也支持环境变量：

- `WX_APPID`
- `WX_APPSECRET`
- `WX_AUTHOR`
- `WX_PROXY`（HTTP/SOCKS5 代理）

---

## 注意事项

- 仅推送到草稿箱，**不会直接发布**
- 需要在公众号后台将服务器 IP 加入白名单
- 封面图尺寸 `900×383`（2.35:1）
- 发布前建议先看图文预览再确认
- 发布脚本已改用纯 Python 实现，不再依赖 `curl`

---

## 字体与版权

- 封面默认字体：`assets/NotoSansCJKsc-Bold.otf`
- 字体来源：[思源黑体 / Noto CJK](https://github.com/googlefonts/noto-cjk)
- 字体协议：**SIL Open Font License**（可商用，按协议使用）
- 跨平台自动查找：macOS (PingFang SC) → Windows (Microsoft YaHei) → Linux (Noto Sans CJK SC) → 内置字体

---

## License

MIT
