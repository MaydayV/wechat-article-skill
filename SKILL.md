---
name: wechat-article
description: Create, format, and publish WeChat Official Account (微信公众号) articles to draft box with stable quality gates (config bootstrap, metadata validation, cover style×palette presets, and publish preflight). Use when user asks to write/format/publish a WeChat article, generate cover image, or push content to 公众号草稿箱.
---

# 微信公众号文章创作（稳定版）

## 配置文件

统一使用工作区 `wechat-article.config.json`：

```json
{
  "appid": "公众号 AppID",
  "appsecret": "公众号 AppSecret",
  "author": "默认作者名",
  "account_name": "公众号名称",
  "slogan": "公众号 Slogan",
  "writing": {
    "perspective": "第一人称",
    "tone": "口语化",
    "length": "1500-2500字",
    "direction": "科技/AI/产品思考",
    "keywords_style": "短句为主，一行不超过30字",
    "article_style": "default",
    "style_profile": "auto",
    "reference_articles": []
  },
  "publish": {
    "need_open_comment": 1,
    "only_fans_can_comment": 0
  },
  "cover": {
    "html_template": null,
    "default_style": "minimal-grid",
    "palette": "auto",
    "rotate": "sequential",
    "seed": "title",
    "allowed_styles": ["minimal-grid", "card-editorial", "diagonal-motion", "soft-gradient"],
    "allowed_palettes": ["blue-tech", "purple-insight", "green-growth", "orange-energy", "rose-story", "slate-pro"]
  },
  "preview": {
    "send_cover_preview": 1,
    "require_confirm_before_publish": 1,
    "confirm_keyword": "确认发布"
  },
  "branding": {
    "header_html": "",
    "footer_html": ""
  },
  "article_reader": {
    "method": "auto",
    "methods_priority": ["camoufox", "jina_reader", "browser_snapshot"],
    "camoufox": {
      "enabled": true,
      "path": "~/.agent-reach/tools/wechat-article-for-ai/main.py"
    },
    "jina_reader": {
      "enabled": true
    },
    "browser_snapshot": {
      "enabled": true
    }
  }
}
```

### 首次使用

若配置不存在，先问完并写入：
1. `appid` / `appsecret`
2. `account_name` / `slogan` (必填)
3. 默认作者
4. 写作风格（视角、语气、长度、方向）
5. 排版风格（默认 `default`，可选 `gougestyle`）
6. 评论开关（默认：开放评论=1，仅粉丝可评=0）
7. 封面策略（HTML 模板或 PIL 方案）
8. **写作风格DNA初始化**：
   - 询问用户是否有喜欢的公众号文章（3-5篇最佳）
   - 如果有，让用户提供链接，系统自动抓取并分析
   - 如果没有，使用默认风格，后续在创作交互中逐步学习
9. 文章读取能力检测：
   - 检测 Camoufox 是否可用（`~/.agent-reach/tools/wechat-article-for-ai/main.py`）
   - 如果不可用，提示安装或降级到其他方案

若内置预览图不存在或需要更新，再执行：

```bash
python3 scripts/create_cover_preview_grid.py
```

将预览图发给用户后，必须用**中文+编号**询问（不要英文术语裸露给用户）：

- A. 默认风格（4选1）
  - A1 极简网格（minimal-grid）
  - A2 编辑卡片（card-editorial）
  - A3 斜切动势（diagonal-motion）
  - A4 柔和渐变（soft-gradient）

- B. 配色策略（2选1）
  - B1 自动轮换配色（palette=auto，推荐）
  - B2 固定单一配色（从 C 区再选 1 套）

- C. 配色方案（6选1，仅在 B2 时必选）
  - C1 科技蓝（blue-tech）
  - C2 洞察紫（purple-insight）
  - C3 增长绿（green-growth）
  - C4 活力橙（orange-energy）
  - C5 故事玫红（rose-story）
  - C6 专业灰（slate-pro）

- D. 轮换方式（2选1，仅在 B1 时必选）
  - D1 顺序轮换（sequential，推荐）
  - D2 随机轮换（random）

用户回复格式：`A2 B1 D1` 或 `A1 B2 C3`。

然后把选择结果持久化到 `wechat-article.config.json` 的 `cover` 字段。

### 后续使用

配置存在时：用户给主题即可，按流程执行「创作 → 排版 → 封面 → 预览确认 → 草稿发布」。

## 写作风格DNA系统

### 核心理念

每个用户的写作风格来自自己的参考文章，而不是公共模板。这确保即使100个人用同一个 skill，每个人的输出都不同。

### DNA 文件

- **模板**：`references/style-dna-template.md`（空白模板，首次使用时复制）
- **用户DNA**：`references/style-dna.md`（系统生成+持续更新）
- **参考文章**：`references/my-articles/`（用户提供的参考文章）

### DNA 初始化流程

```
用户提供 3-5 篇喜欢的公众号文章链接
    ↓
系统通过 article_reader 抓取文章内容
    ↓
保存到 references/my-articles/
    ↓
分析所有参考文章，提取风格特征：
- 句子平均长度
- 常用句式（反问？排比？短句连击？）
- 金句结构（比喻型？数字型？对比型？）
- 开头偏好（故事？数据？场景？）
- 结尾偏好（号召？金句？悬念？）
- 高频词汇和禁用词
- 段落结构和节奏
    ↓
生成 references/style-dna.md
    ↓
展示给用户确认/调整
```

### DNA 持续进化

每次创作交互中，系统根据用户反馈自动更新 DNA：

| 用户行为 | DNA 更新 |
|---------|---------|
| "这个开头太平了" | 记录：avoid 平铺直叙开头 |
| "这个金句好" | 记录：preferred 该句式模式 |
| 用户手动改了某段 | 对比改前改后，提取偏好变化 |
| 用户选了标题B而不是A | 记录标题偏好 |
| "别用这种表达" | 加入 avoid_phrases |
| "我喜欢这种感觉" | 提取特征加入 preferred |

**更新规则（建议确认模式）：**
- 每次创作结束后，检查是否有新的偏好信号
- 如果有，**先向用户展示建议的 DNA 更新内容**，用户确认后才写入
- 默认不自动覆盖，防止"DNA 漂移"（把偶然偏好当成固定风格）
- 用户手动调整过的字段优先级最高，不会被自动建议覆盖

### 反模板化检测

生成文章后，自动检查：
- ❌ 是否出现 DNA 中 `avoid_phrases` 列表里的表达
- ❌ 是否与 `recent_golden_phrases` 中的金句重复率 > 30%
- ❌ 是否与最近3篇文章使用了相同的开头/结尾结构
- ❌ 是否段落结构与最近一篇完全一致

如果检测到，自动重新生成该部分，使用不同的表达方式。

## 公众号文章读取

### 读取方案（多层降级）

当用户提供公众号文章链接时，按以下优先级读取：

**1. Camoufox（首选，最稳定）**
```bash
cd ~/.agent-reach/tools/wechat-article-for-ai && python3 main.py "https://mp.weixin.qq.com/s/xxx"
```
- 能绕过微信反爬机制
- 输出 markdown 格式，包含标题、作者、日期、正文
- 需要预先安装

**2. Jina Reader（备选）**
```bash
curl -s "https://r.jina.ai/https://mp.weixin.qq.com/s/xxx"
```
- 部分文章可能被拦截

**3. Browser Snapshot（兜底）**
- 使用 OpenClaw 的 browser 工具打开链接
- 提取页面文本内容

**4. 手动粘贴（最终兜底）**
- 提示用户手动复制文章内容

### 读取能力检测

首次使用时自动检测：
```bash
# 检测 Camoufox
python3 ~/.agent-reach/tools/wechat-article-for-ai/main.py --help 2>/dev/null
```

如果不可用，提示用户：
- 安装 agent-reach skill 以获得最佳文章读取能力
- 或降级使用其他方案

## 工作流（必须按顺序）

复制并勾选：

```text
WeChat Article Progress:
- [ ] Step 0: 读取/初始化配置 + 加载风格DNA
- [ ] Step 1: 生成文章内容（基于风格DNA）
- [ ] Step 2: 产出 HTML（内联样式 + 页头页脚）
- [ ] Step 3: 校验元数据（标题/摘要/作者）
- [ ] Step 4: 生成封面图
- [ ] Step 4.5: 生成正文配图（可选）
- [ ] Step 5: 发送预览（文本 + 封面图）并等待确认
- [ ] Step 6: 发布前预检（凭证/依赖/文件）
- [ ] Step 7: 推送草稿
- [ ] Step 8: 返回结果 + 更新风格DNA
```

### Step 0: 读取/初始化配置 + 加载风格DNA

- 读取 `wechat-article.config.json`
- 不存在则进入首次配置并写入
- 配置存在但缺字段：只补缺失字段，不覆盖用户已有偏好
- 读取 `references/style-dna.md`
  - 如果不存在且用户提供了参考文章，先执行 DNA 初始化
  - 如果不存在且无参考文章，使用 `writing.*` 配置作为基础风格

### Step 1: 生成文章内容（基于风格DNA）

#### 1a. 选择文章结构

**不要默认使用"开头 → 3-5小节 → 结尾"。** 根据 `references/structures.md` 中的选择规则，按主题类型选择结构原型：
- 赚钱/变现 → 时间线叙事
- 技术/工具 → 标准分节 或 清单体
- 观点/洞察 → 问答对话体
- 经验/复盘 → 时间线叙事
- 推荐/盘点 → 清单体

**反重复规则：** 检查 DNA 中 `recent_articles` 的最近2篇结构，如果相同则强制切换。

#### 1b. 加载风格DNA和个人素材

**如果存在 `references/style-dna.md`：**
- 严格按照 DNA 中定义的风格特征生成内容
- 模仿 DNA 中记录的句式、节奏和表达习惯
- 避免 DNA 中 `avoid_phrases` 和 `avoid_patterns` 列出的表达
- 检查 `recent_golden_phrases`，确保不重复使用金句
- 根据主题类型，参考 DNA 中的 `主题风格映射` 调整语言风格

**如果存在 `references/story-bank.md`：**
- 优先从用户的真实经历库中选取与主题相关的素材
- 用真实观点替代 AI 编造的观点
- 使用用户的口头禅和语言习惯
- 参考用户的情绪色板调整文章情绪基调

**如果不存在 DNA：**
- 按配置中的 `writing.*` 产出正文

#### 1c. 内容安全意识

生成时主动遵守 `references/content-safety.md` 中的规则：
- 识别当前主题是否属于高/中风险话题
- 高风险话题自动切换为安全写法（"信息整理"模式，不做主观建议）
- 涉及具体数据时，区分"硬事实"和"软观点"：
  - 硬事实（具体数字、排名、统计）：必须标注来源，无来源则改为模糊表述
  - 软观点（个人判断、经验分享）：可以直接表达，但用"个人经验"限定
- 禁止使用 `content-safety.md` 中列出的禁止声明

#### 1d. 降低模板感

- 段落长度要有变化：短段（1-2句）和长段（5-8句）交替出现
- 不要每段都在"输出价值"，适当留白和过渡
- 每隔 400-600 字设置一个"小钩子"（反问、悬念、转折），保持阅读动力
- 如果有个人素材库，在合适位置插入真实细节增加"人味"

约束：
- 标题建议 ≤ 20 个中文字符（传播友好）
- 正文建议 ≤ 1000~2500 字（按用户配置）

### Step 2: 产出 HTML（内联样式 + 页头页脚）

严格按 `references/styles/{article_style}.md` 定义的排版规范。
- 外层 `<section>`
- 正文 `<p>`
- 重点 `<strong>`
- 章节间 `<hr>`
- 不输出 markdown，不依赖外部 CSS
- 如果配置了 `branding.header_html` 或 `branding.footer_html`，将其插入到文章内容 HTML 的对应位置。

### Step 3: 校验元数据

发布前必须有：
- `title`（不能为空）
- `digest`（建议 ≤ 120 字）
- `author`（优先配置 author）

回填顺序：
1. 用户显式给定
2. 配置默认值
3. 自动生成（标题取主标题，摘要取首段压缩）

### Step 4: 生成封面图

**核心原则：每篇文章封面必须根据主题设计，不能重复使用同一套视觉风格。**

优先级：
1. 用户提供 `cover_path`
2. 使用 `cover.html_template` 指定的 HTML 模板，结合 Playwright 截图（推荐）
   - 可用模板：`akai-cover` (阿凯封面模板), `gouge-cover` (狗哥封面模板)
3. 回退到 PIL 方案，使用 `cover.default_style` 和 `cover.palette`

#### HTML + Playwright 截图方案 (推荐)

根据 `cover.html_template` 配置，渲染 `/templates/covers/{template_name}.html`，并使用 Playwright 截图。
- 参数：`--html-template`, `--title`, `--subtitle`, `--account-name`, `--slogan`, `--tag`

#### PIL 降级方案

如果未指定 `cover.html_template`，则使用 `scripts/create_cover.py` 进行 PIL 图像生成。
- 参数：`--title`, `--subtitle`, `--style`, `--palette`, `--rotate`, `--seed`

命令参数优先级：
1. 用户本次明确指定
2. 配置 `cover.*`
3. 脚本默认值

### Step 4.5: 生成正文配图（可选）

根据文章内容，可以生成配图增强可读性。
- 使用 `scripts/illustrations/` 目录下的脚本生成图片（例如：`generate_concept.py`, `generate_flow.py`, `generate_table.py`）。
- 生成的图片需通过 `publish_draft.py` 的 `--content-img KEY=PATH` 参数上传。
- 在 `article.html` 中使用 `<!-- IMAGE_KEY -->` 占位符，脚本会自动替换为上传后的图片 URL。

### Step 5: 发送预览（文本 + 封面图）并等待确认

在推送草稿前，必须先给用户看预览：

预览内容至少包含：
- 标题
- 摘要
- 作者
- 封面图（本次生成的 cover 文件）
- 正文预览（前 2-3 段或前 200-300 字）

发送规则：
- 若当前渠道支持图片，发送"文字 + 封面图"
- 预览文案必须中文，且包含明确操作提示：
  - `确认发布`（继续）
  - `修改封面`（仅重做封面）
  - `修改正文`（回到正文编辑）

确认策略（默认）：
- `preview.require_confirm_before_publish = 1` 时，未收到 `preview.confirm_keyword`（默认 `确认发布`）前，不得执行发布
- 若用户回复 `修改封面`，保留正文，重新执行 Step 4 后再次预览
- 若用户回复 `修改正文`，回到 Step 1/2 调整后再次预览

### Step 6: 发布前预检

发布前必须检查：
1. `python3` 可用
2. `Pillow` 已安装（若需生成封面或配图）
3. `Playwright` 及其浏览器驱动已安装（若使用 HTML 模板封面）
4. `appid/appsecret` 非空
5. `article.html` 与封面文件存在
6. **内容安全校验**（必须执行）：

```bash
python3 scripts/validate_article.py --content-file article.html
```

校验结果处理：
- `risk_score = 0`，`can_publish = true` → 直接进入 Step 7
- `needs_review = true`（有警告）→ 将校验报告展示给用户，标注待核实的数据和中风险内容，用户确认后才能继续
- `can_publish = false`（有错误）→ **阻断发布**，展示具体问题，要求用户修改后重新校验

缺项时先修复，不要直接发布。

### Step 7: 推送草稿

使用 `scripts/publish_draft.py`。

```bash
python3 scripts/publish_draft.py \
  --title "文章标题" \
  --author "作者名" \
  --digest "摘要（120字内）" \
  --content-file article.html \
  --cover cover.jpg \
  --appid <appid> \
  --appsecret <appsecret> \
  --need-open-comment 1 \
  --only-fans-can-comment 0 \
  --header-img <页眉图片路径> \
  --content-img <KEY1=PATH1> --content-img <KEY2=PATH2>
```

评论参数优先级：
1. 用户这次明确要求
2. 配置 `publish.*`
3. 默认值（1 / 0）

### Step 8: 返回结果 + 更新风格DNA

固定返回：
- 标题、摘要、作者
- 封面文件 + 使用的风格/配色
- 评论开关状态
- 草稿 `media_id`
- 已上传的正文图片 URL 列表
- 下一步：去公众号后台「内容管理 → 草稿箱」预览并发布

**DNA 更新（如果存在 style-dna.md）：**
- 将本次文章标题加入 `recent_articles`
- 将本次使用的开头/结尾类型加入历史记录
- 将本次使用的金句加入 `recent_golden_phrases`
- 如果用户在创作过程中有反馈（修改、选择、评价），更新对应的偏好字段
- 在更新日志中记录本次变更

## 安全与边界

- 仅推送草稿箱，不直接群发
- 凭证只存本地配置，不写进技能文件
- 任何外发动作（自动发布/群发）必须单独征求用户确认

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
│   ├── structures.md                 (文章结构原型库)
│   ├── content-safety.md             (内容安全与合规指南)
│   ├── style-dna-template.md         (风格DNA空白模板)
│   ├── story-bank-template.md        (个人素材库模板)
│   ├── style-dna.md                  (用户风格DNA，系统生成)
│   ├── story-bank.md                 (用户个人素材库)
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
    ├── validate_article.py           (发布前内容校验)
    └── illustrations/
        ├── generate_concept.py       (概念示意图生成)
        ├── generate_flow.py          (流程图生成)
        ├── generate_header.py        (页眉图片生成)
        └── generate_table.py         (数据表格图生成)
```
