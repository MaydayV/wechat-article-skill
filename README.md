<p align="center">
  <h1 align="center">wechat-article-skill</h1>
  <p align="center">
    <strong>一句话，一篇文章，一键草稿箱。</strong><br/>
    你的文字风格是你的指纹，AI 只是替你握笔。
  </p>
</p>

<p align="center">
  <a href="#快速开始">快速开始</a> •
  <a href="#写作风格-dna">风格 DNA</a> •
  <a href="#封面系统">封面系统</a> •
  <a href="#与-ai-编程工具集成">Claude / Codex 集成</a> •
  <a href="#项目结构">项目结构</a>
</p>

---

## 这是什么？

一个面向微信公众号的 AI 写作引擎。不是又一个"帮你写文章"的工具——

它会**学习你的写作风格**，然后用你的方式写。

```
你：写一篇关于 AI 创业的文章
↓
系统读取你的风格 DNA → 生成文章 → 排版 → 封面 → 预览 → 一键推送草稿箱
```

用得越多，它越像你。

---

## 核心能力

| 能力 | 说明 |
|------|------|
| 🧬 **风格 DNA** | 从你的参考文章中提取写作指纹，每个人的输出天然不同 |
| ✍️ **一句话创作** | 给个主题，出完整文章。标题、正文、摘要、封面一步到位 |
| 📖 **公众号文章抓取** | 丢个链接进来，自动读取全文内容（微信反爬？不存在的） |
| 🎨 **封面生成** | HTML 模板 + Playwright 截图，或 PIL 纯图像方案，4 风格 × 6 配色 |
| 📝 **微信排版** | 内联 CSS，适配微信编辑器，多种排版风格可选 |
| 🖼️ **配图生成** | 概念图、流程图、数据表格，命令行一键生成 |
| 🔄 **持续进化** | 每次交互自动学习你的偏好，DNA 越用越准 |
| 🚀 **草稿推送** | 纯 Python 实现，上传封面 + 正文图片 + 创建草稿，零外部依赖 |

---

## 快速开始

### 搭配 OpenClaw 使用（推荐）

```bash
# 1. 克隆到 skills 目录
git clone https://github.com/MaydayV/wechat-article-skill.git ~/.openclaw/skills/wechat-article-skill

# 2. 在对话中直接说
帮我写一篇公众号文章，主题是「一个人如何用 AI 做一家公司」
```

首次使用会自动引导你完成配置：AppID、公众号名称、写作风格、封面偏好、风格 DNA 初始化。

### 搭配 Claude Code 使用

```bash
# 在 Claude Code 中加载 skill
claude --skill ~/.openclaw/skills/wechat-article-skill/SKILL.md

# 然后直接对话
> 读取我的风格 DNA，写一篇关于 AI Agent 的文章，推送到草稿箱
```

### 搭配 Codex CLI 使用

```bash
# Codex 可以直接读取 SKILL.md 作为系统指令
codex --system-prompt "$(cat ~/.openclaw/skills/wechat-article-skill/SKILL.md)" \
  "帮我写一篇公众号文章，主题是 AI 时代的个人品牌"
```

### 纯脚本使用（不依赖任何 AI 框架）

```bash
pip3 install Pillow jinja2 playwright && playwright install chromium

# 生成封面
python3 scripts/create_cover.py --title "标题" --subtitle "副标题" --style minimal-grid --output cover.jpg

# 推送草稿
python3 scripts/publish_draft.py --title "标题" --content-file article.html --cover cover.jpg --appid $WX_APPID --appsecret $WX_APPSECRET
```

---

## 写作风格 DNA

> 公共模板用的人越多，大家的文章越像。
> 风格 DNA 让每个人的输出天然不同——因为你的参考文章，只属于你。

### 它怎么工作？

```
你丢进来 3-5 篇喜欢的文章（自己写的，或别人写的）
    ↓
系统自动分析：句式节奏、金句结构、开头偏好、结尾习惯、高频词汇
    ↓
生成你的专属 style-dna.md
    ↓
后续每篇文章都基于这个 DNA 生成
    ↓
每次交互持续进化：你的反馈 = DNA 的升级
```

### DNA 进化示例

| 你的行为 | DNA 的反应 |
|---------|-----------|
| "这个开头太平了" | 标记：避免平铺直叙 |
| "这个金句不错" | 提取句式模式，加入偏好 |
| 选了标题 B 而不是 A | 记录标题偏好倾向 |
| 手动改了某段话 | 对比前后差异，提取风格变化 |
| "别用'赋能'这种词" | 加入禁用词列表 |

### 反模板化检测

每篇文章生成后自动检查：
- ❌ 是否出现禁用表达
- ❌ 是否与最近 3 篇使用了相同的开头/结尾结构
- ❌ 金句重复率是否 > 30%

检测到就自动重写，确保每篇都有新鲜感。

---

## 封面系统

### HTML 模板方案（推荐）

Playwright 渲染 + 截图，视觉效果拉满。

| 模板 | 风格 | 预览 |
|------|------|------|
| `akai-cover` | 极简白底、左侧渐变竖线、大标题居左 | 适合深度思考类 |
| `gouge-cover` | 深色科技风、网格背景、光晕装饰 | 适合技术/产品类 |

```bash
python3 scripts/create_cover.py \
  --html-template templates/covers/akai-cover.html \
  --title "文章标题" --subtitle "副标题" \
  --account-name "你的公众号" --slogan "你的 Slogan" \
  --output cover.jpg
```

### PIL 方案（轻量降级）

不需要浏览器环境，纯 Python 生成。

**4 种风格：**
`minimal-grid` · `card-editorial` · `diagonal-motion` · `soft-gradient`

**6 套配色：**
`blue-tech` · `purple-insight` · `green-growth` · `orange-energy` · `rose-story` · `slate-pro`

支持自动轮换配色，确保每篇封面都不一样。

---

## 排版风格

| 风格 | 字号 | 行高 | 对齐 | 特点 |
|------|------|------|------|------|
| `default` | 16px | 2.0 | 两端对齐 | 标准公众号排版 |
| `gougestyle` | 15px | 1.75 | 左对齐 | 微信兼容优化，阅读更舒适 |

自定义风格：在 `references/styles/` 下新建 `.md` 文件即可。

---

## 配图生成

内置 4 种配图脚本，所有参数通过命令行传入，跨平台字体自动查找。

```bash
# 概念示意图
python3 scripts/illustrations/generate_concept.py \
  --title "OPC = 你 + AI" --left-label "你" --right-label "AI" --output concept.jpg

# 流程图
python3 scripts/illustrations/generate_flow.py \
  --title "三步启动" --steps "注册:在线办理" "找政策:入驻社区" "验证:用AI跑通" --output flow.jpg

# 数据表格
python3 scripts/illustrations/generate_table.py \
  --title "城市政策对比" --headers "城市,政策,补贴" \
  --rows "深圳,训力券,最高1000万;上海,免租,10万启动金" --output table.jpg

# 页眉
python3 scripts/illustrations/generate_header.py \
  --title "你的公众号" --slogan "你的 Slogan" --output header.jpg
```

---

## 公众号文章读取

丢一个公众号链接进来，系统自动抓取全文。

**四层降级，总有一个能用：**

| 优先级 | 方案 | 说明 |
|--------|------|------|
| 1 | Camoufox | 最稳定，绕过微信反爬 |
| 2 | Jina Reader | 轻量级，部分文章可能被拦截 |
| 3 | Browser Snapshot | OpenClaw 内置浏览器提取 |
| 4 | 手动粘贴 | 兜底方案 |

---

## 项目结构

```text
wechat-article-skill/
├── SKILL.md                          # 核心指令文件（AI 读这个）
├── README.md
├── assets/
│   ├── NotoSansCJKsc-Bold.otf        # 思源黑体（SIL OFL，可商用）
│   └── cover-style-palette-preview-grid.jpg
├── references/
│   ├── article-style.md              # 排版风格索引
│   ├── style-dna-template.md         # 风格 DNA 空白模板
│   ├── style-dna.md                  # 你的风格 DNA（自动生成）
│   ├── my-articles/                  # 你的参考文章
│   └── styles/
│       ├── default.md
│       └── gougestyle.md
├── templates/covers/
│   ├── akai-cover.html               # 阿凯封面模板
│   └── gouge-cover.html              # 狗哥封面模板
└── scripts/
    ├── font_utils.py                 # 跨平台字体工具
    ├── create_cover.py               # 封面生成
    ├── create_cover_preview_grid.py   # 封面预览网格
    ├── publish_draft.py              # 草稿发布（纯 Python）
    └── illustrations/
        ├── generate_concept.py       # 概念图
        ├── generate_flow.py          # 流程图
        ├── generate_header.py        # 页眉
        └── generate_table.py         # 数据表格
```

---

## 环境变量

| 变量 | 说明 |
|------|------|
| `WX_APPID` | 公众号 AppID |
| `WX_APPSECRET` | 公众号 AppSecret |
| `WX_AUTHOR` | 默认作者名 |
| `WX_PROXY` | HTTP/SOCKS5 代理地址 |

---

## 注意事项

- 仅推送到草稿箱，**不会直接发布**
- 需要在公众号后台将服务器 IP 加入白名单
- 封面图尺寸 `900×383`（2.35:1）
- 发布脚本纯 Python 实现，不依赖 `curl`
- 风格 DNA 和参考文章是用户私有数据，不会被提交到仓库（`.gitignore` 已配置）

---

## 字体与版权

- 内置字体：[思源黑体 / Noto Sans CJK SC](https://github.com/googlefonts/noto-cjk)（SIL Open Font License，可商用）
- 跨平台自动查找：macOS → Windows → Linux → 内置字体

---

## License

MIT
