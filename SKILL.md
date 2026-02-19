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
- [ ] Step 2: 产出 HTML（内联样式）
- [ ] Step 3: 校验元数据（标题/摘要/作者）
- [ ] Step 4: 生成或解析封面图（style × palette）
- [ ] Step 5: 发送预览（文本 + 封面图）并等待确认
- [ ] Step 6: 发布前预检（凭证/依赖/文件）
- [ ] Step 7: 推送草稿
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

严格按 `references/article-style.md`：
- 外层 `<section>`
- 正文 `<p>`（16px, line-height 2）
- 重点 `<strong style="color:#1a73e8;">`
- 章节间 `<hr>`
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

### Step 4: 生成或解析封面图（style × palette）

优先级：
1. 用户提供 cover 路径
2. 项目目录 `imgs/cover.png`（若存在）
3. 运行 `scripts/create_cover.py` 生成 `cover.jpg`

风格：
- `minimal-grid`
- `card-editorial`
- `diagonal-motion`
- `soft-gradient`

配色：
- `blue-tech`
- `purple-insight`
- `green-growth`
- `orange-energy`
- `rose-story`
- `slate-pro`
- `auto`（按 `rotate` 策略选色）

生成命令（默认）

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

命令参数优先级：
1. 用户本次明确指定
2. 配置 `cover.*`
3. 脚本默认值

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
1. `python3` 可用
2. `curl` 可用（发布脚本依赖）
3. `Pillow` 已安装（若需生成封面）
4. `appid/appsecret` 非空
5. `article.html` 与封面文件存在

缺项时先修复，不要直接发布。

### Step 7: 推送草稿

使用：

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
  --only-fans-can-comment 0
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
