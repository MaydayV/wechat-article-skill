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
  "slogan": "公众号 slogan",
  "writing": {
    "perspective": "第一人称",
    "tone": "口语化",
    "length": "1500-2500字",
    "direction": "科技/AI/产品思考",
    "keywords_style": "短句为主，一行不超过30字"
  },
  "publish": {
    "need_open_comment": 1,
    "only_fans_can_comment": 0
  },
  "cover": {
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
    "header_html": "<页头 HTML，每篇文章顶部自动插入>",
    "footer_html": "<页脚 HTML，每篇文章底部自动插入>"
  }
}
```

### 首次使用

若配置不存在，先问完并写入：
1. `appid` / `appsecret`
2. 默认作者
3. 写作风格（视角、语气、长度、方向）
4. 评论开关（默认：开放评论=1，仅粉丝可评=0）
5. 优先使用内置预览图（`assets/cover-style-palette-preview-grid.jpg`）展示风格×配色，让用户选择默认风格
6. 写入封面策略（默认 `palette=auto`, `rotate=sequential`, `seed=title`）

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

## 工作流（必须按顺序）

复制并勾选：

```text
WeChat Article Progress:
- [ ] Step 0: 读取/初始化配置
- [ ] Step 1: 生成文章内容
- [ ] Step 2: 产出 HTML（内联样式 + 页头页脚）
- [ ] Step 3: 校验元数据（标题/摘要/作者）
- [ ] Step 4: 生成或解析封面图（style × palette）
- [ ] Step 4.5: 生成正文配图（可选）
- [ ] Step 5: 发送预览（文本 + 封面图）并等待确认
- [ ] Step 6: 发布前预检（凭证/依赖/文件）
- [ ] Step 7: 推送草稿（含配图上传）
- [ ] Step 8: 返回结果与下一步
```

### Step 0: 读取/初始化配置

- 读取 `wechat-article.config.json`
- 不存在则进入首次配置并写入
- 配置存在但缺字段：只补缺失字段，不覆盖用户已有偏好
- 若 `cover.default_style` 缺失：
  1) 优先使用 `assets/cover-style-palette-preview-grid.jpg` 作为预览图
  2) 若该图不存在，再运行 `python3 scripts/create_cover_preview_grid.py` 生成
  3) 给用户看图并让其选择默认风格
  4) 把选择写回 `cover.default_style`

### Step 1: 生成文章内容

按配置中的 `writing.*` 产出正文。

约束：
- 标题建议 ≤ 20 个中文字符（传播友好）
- 正文建议 ≤ 1000~2500 字（按用户配置）
- 结构优先：开场、3-5 个小节、结尾行动建议

### Step 2: 产出 HTML（内联样式）

严格按 `references/article-style.md`（2026版排版规范）：

**外层容器：**
```html
<section style="font-family: -apple-system, BlinkMacSystemFont, 'PingFang SC', 'Helvetica Neue', Arial, sans-serif; max-width: 677px; margin: 0 auto; padding: 0 20px; color: #3f3f3f; font-size: 15px; line-height: 1.75;">
```

**关键参数：**
- 正文字号：15px（14-16px范围）
- 行间距：1.75倍（1.5-1.75倍范围）
- 页边距：20px（10-30px范围）
- 正文颜色：#3f3f3f（不用纯黑）
- 段间距：1.5em

**正文段落：**
```html
<p style="margin: 1.5em 0;">文本内容</p>
```

**小标题：**
```html
<p style="margin: 1.5em 0; font-size: 18px; font-weight: bold; color: #2e6e9e;">章节标题</p>
```

**重点强调：**
- 蓝色强调：`<strong style="color:#3daad6;">重点内容</strong>`
- 深蓝强调：`<strong style="color:#2e6e9e;">重点内容</strong>`
- 橙色强调（数字/金额）：`<strong style="color:#f79646;">1000万元</strong>`

**分隔线：**
```html
<hr style="border: none; border-top: 1px solid #eee; margin: 2em 0;" />
```

**页头页脚（微信兼容写法）：**

页头使用 `<table>` 布局（已验证在微信中可正常渲染，`<div>` 背景色会被过滤）：

```html
<table width="100%" cellpadding="0" cellspacing="0" style="background-color: #1a3a5c; border-radius: 8px; margin-bottom: 24px;">
  <tr>
    <td style="padding: 20px; text-align: center;">
      <p style="margin: 0 0 6px 0; font-size: 10px; letter-spacing: 3px; color: #7a9ab8; text-align: center;">ORIGINAL CONTENT</p>
      <p style="margin: 0 0 8px 0; font-size: 22px; font-weight: bold; color: #ffffff; text-align: center;">狗哥的胡思乱想</p>
      <p style="margin: 0; font-size: 12px; color: #8ab0cc; text-align: center;">创业 · AI · 那些没人告诉你的事</p>
    </td>
  </tr>
</table>
```

⚠️ 微信CSS限制（已验证）：
- `background-color` 在 `<div>`/`<section>` 上会被过滤，必须用 `<table>` 承载背景色
- `linear-gradient` 渐变不支持，只能用纯色
- `rgba()` 不支持，只能用 hex 实色
- `text-align` 必须加在每个 `<p>` 上，不能靠父元素继承
- `display: flex` 不可靠，用 `<table>` 替代布局

**排版原则：**
- 每隔三行另起一段
- 长文居左对齐
- 短句用 `<br />` 换行，不要每句都开新段落
- 不输出 markdown，不依赖外部 CSS

### Step 3: 校验元数据

发布前必须有：
- `title`（不能为空）
- `digest`（建议 ≤ 120 字）
- `author`（优先配置 author）

回填顺序：
1. 用户显式给定
2. 配置默认值
3. 自动生成（标题取主标题，摘要取首段压缩）

### Step 4: 生成封面图（HTML+Playwright 截图方案）

**核心原则：每篇文章封面必须根据主题设计，不能重复使用同一套视觉风格。**

优先级：
1. 用户提供 cover 路径
2. 项目目录 `imgs/cover.png`（若存在）
3. 用 HTML+Playwright 截图生成（推荐，效果最好）
4. 降级：运行 `scripts/create_cover.py` 生成（PIL方案，效果较差）

#### HTML+Playwright 截图方案（推荐）

根据文章主题设计 `cover_design.html`，然后用 Playwright 截图：

```python
from playwright.sync_api import sync_playwright
import os

html_path = os.path.abspath('cover_design.html')
with sync_playwright() as p:
    browser = p.chromium.launch()
    page = browser.new_page(viewport={'width': 900, 'height': 383})
    page.goto('file:///' + html_path.replace('\\', '/'))
    page.wait_for_timeout(500)
    page.screenshot(path='cover.jpg', clip={'x':0,'y':0,'width':900,'height':383})
    browser.close()
```

**封面尺寸：900×383px（微信公众号标准比例）**

#### 封面设计原则

每篇文章根据主题选择不同的视觉方向：

| 文章类型 | 推荐风格 | 配色方向 |
|---------|---------|---------|
| 科技/教程 | 深色科技网格 + 几何装饰 | 深蓝底 + 青色高亮 |
| 创业/商业 | 简洁卡片 + 大字排版 | 白底/深色 + 品牌色 |
| AI/未来 | 渐变光晕 + 粒子感 | 紫蓝渐变 |
| 生活/故事 | 温暖插画风 | 暖色系 |

**必须包含：**
- 文章主标题（大字，视觉重心）
- 副标题或定位标签
- 账号署名（低调放置）

**禁止：**
- 每篇文章用同一套模板
- 背景纯色无设计感
- 字体太小看不清

#### PIL 降级方案

```bash
python3 scripts/create_cover.py \
  --title "主标题" \
  --subtitle "副标题" \
  --style "minimal-grid" \
  --palette "auto" \
  --rotate "sequential" \
  --seed "主标题" \
  --output cover.jpg
```

可用风格：`minimal-grid` / `card-editorial` / `diagonal-motion` / `soft-gradient`
可用配色：`blue-tech` / `purple-insight` / `green-growth` / `orange-energy` / `rose-story` / `slate-pro`

### Step 4.5: 生成正文配图（可选）

根据文章内容，可以生成配图增强可读性：

**配图类型：**
1. **数据可视化图表**：政策对比表、数据统计图
2. **概念示意图**：流程图、架构图、关系图
3. **场景插图**：用Python PIL生成或AI生成

**生成方式：**
- 使用Python PIL库生成表格、图表
- 使用matplotlib生成数据可视化
- 使用AI工具（如Gemini）生成概念图

**配图规范：**
- 尺寸：宽度建议900-1200px
- 格式：JPG（质量95）
- 文件名：描述性命名（如 `policy_table.jpg`、`opc_concept.jpg`）
- 保存位置：技能目录下

**插入方式：**
在 `article.html` 中使用占位符：
```html
<!-- IMAGE_POLICY_TABLE -->
```

发布时脚本会自动上传图片并替换占位符。

### Step 5: 发送预览（文本 + 封面图）并等待确认

在推送草稿前，必须先给用户看预览：

预览内容至少包含：
- 标题
- 摘要
- 作者
- 封面图（本次生成的 cover 文件）
- 正文预览（前 2-3 段或前 200-300 字）

发送规则：
- 若当前渠道支持图片，发送“文字 + 封面图”
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
1. `python` 可用
2. `Pillow` 已安装（若需生成封面或配图）
3. `appid/appsecret` 非空
4. `article.html` 与封面文件存在

缺项时先修复，不要直接发布。

注：发布脚本已改用纯Python实现，不再依赖 `curl`。

### Step 7: 推送草稿

使用：

```bash
python scripts/publish_draft.py \
  --title "文章标题" \
  --author "作者名" \
  --digest "摘要（120字内）" \
  --content-file article.html \
  --cover cover.jpg \
  --opc-concept-img opc_concept.jpg \
  --policy-table-img policy_table.jpg \
  --opc-flow-img opc_flow.jpg \
  --appid <appid> \
  --appsecret <appsecret> \
  --need-open-comment 1 \
  --only-fans-can-comment 0
```

**配图参数（可选）：**
- `--opc-concept-img`：OPC概念图
- `--policy-table-img`：政策对比表
- `--opc-flow-img`：流程图
- 其他自定义配图

脚本会自动：
1. 上传封面图到微信素材库（获取 `thumb_media_id`）
2. 上传正文配图到微信服务器（获取图片URL）
3. 替换 `article.html` 中的图片占位符（`<!-- IMAGE_XXX -->`）
4. 创建草稿

**图片占位符规则：**
在 `article.html` 中使用注释占位符：
```html
<!-- IMAGE_OPC_CONCEPT -->
<!-- IMAGE_POLICY_TABLE -->
<!-- IMAGE_OPC_FLOW -->
```

发布脚本会自动替换为：
```html
<p style="text-align: center;"><img src="微信图片URL" style="max-width: 100%; height: auto; display: block; margin: 0 auto;" alt="图片描述"/></p>
```

评论参数优先级：
1. 用户这次明确要求
2. 配置 `publish.*`
3. 默认值（1 / 0）

### Step 8: 返回结果

固定返回：
- 标题、摘要、作者
- 封面文件 + 使用的风格/配色
- 评论开关状态
- 草稿 `media_id`
- 下一步：去公众号后台「内容管理 → 草稿箱」预览并发布

## 安全与边界

- 仅推送草稿箱，不直接群发
- 凭证只存本地配置，不写进技能文件
- 任何外发动作（自动发布/群发）必须单独征求用户确认
