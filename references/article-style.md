# 公众号文章排版样式参考（2026版）

基于公众号排版最佳实践，参考行业标准。

## HTML 排版规范

### 外层容器

```html
<section style="font-family: -apple-system, BlinkMacSystemFont, 'PingFang SC', 'Helvetica Neue', Arial, sans-serif; max-width: 677px; margin: 0 auto; padding: 0 20px; color: #3f3f3f; font-size: 15px; line-height: 1.75;">
  <!-- 文章内容 -->
</section>
```

关键参数：
- `max-width: 677px` — 公众号标准宽度
- `padding: 0 20px` — 页边距 20px（10-30px范围内）
- `color: #3f3f3f` — 正文颜色（不用纯黑#000）
- `font-size: 15px` — 正文字号（14-16px范围内）
- `line-height: 1.75` — 行间距1.75倍（1.5-1.75倍范围内）

### 正文段落 `<p>`

```html
<p style="margin: 1.5em 0; text-align: left;">
  文本内容
</p>
```

关键属性：
- `margin: 1.5em 0` — 段间距（每隔三行另起一段）
- `text-align: left` — 长文居左对齐

### 短句换行

同一段落内的短句换行用 `<br />`：

```html
<p style="margin: 1.5em 0;">
  代码不会写？AI帮你写。<br />
  设计不会做？AI帮你做。<br />
  市场分析不会？AI帮你跑数据。
</p>
```

### 重点强调句

用 `<strong>` + 蓝色（`#2e6e9e` 或 `#3daad6`）高亮关键观点：

```html
<strong style="color: #2e6e9e;">这是重点内容</strong>
```

可选颜色：
- `#2e6e9e` — 深蓝（推荐用于标题）
- `#3daad6` — 浅蓝（推荐用于正文强调）
- `#f79646` — 橙色（用于特别强调）

### 小标题

```html
<p style="margin: 1.5em 0; font-size: 18px; font-weight: bold; color: #2e6e9e;">
  章节标题
</p>
```

### 分隔线 `<hr>`

用于分隔文章的逻辑段落/章节：

```html
<hr style="border: none; border-top: 1px solid #eee; margin: 2em 0;" />
```

### 注释/说明文字

```html
<p style="margin: 1.5em 0; font-size: 13px; color: #a5a5a5;">
  注释说明文字
</p>
```

### 排版原则（4个准则）

1. **排版并得好，文章发的早** — 排版和目标人群兴趣匹配，没有普适的排版，只有适合的排版
2. **要有辨识度，但不要过于装饰** — 排版顺应文章逻辑，而不是反过来
3. **排版要有延续性，不要天天一个样** — 品牌层面风格要统一
4. **每隔三行，另起一段** — 保持阅读节奏
5. **对齐方式：长文居左，短文居中** — 根据内容长度选择

### 配色参考

**标题颜色：**
- `#f79646` — 橙色
- `#3daad6` — 浅蓝
- `#2e6e9e` — 深蓝

**正文颜色：**
- `#3f3f3f` — 主正文（推荐）
- `#4f4f4f` — 次正文
- `#7f7f7f` — 辅助文字
- `#545454` — 备选
- `#595959` — 备选

**注释颜色：**
- `#d99694` — 粉色注释
- `#a5a5a5` — 灰色注释（推荐）

### 封面图规范

- **一级封面**：900×500px
- **二级封面**：200×200px
- **封面图标题**：控制在13字以内显示最好
- **多图配色**：用同样的色块，或者调性一致

## 完整模板

```html
<section style="font-family: -apple-system, BlinkMacSystemFont, 'PingFang SC', 'Helvetica Neue', Arial, sans-serif; max-width: 677px; margin: 0 auto; padding: 0 20px; color: #3f3f3f; font-size: 15px; line-height: 1.75;">

<p style="margin: 1.5em 0;">开头段落。</p>

<p style="margin: 1.5em 0;">第二段。<br />短句换行。</p>

<p style="margin: 1.5em 0;"><strong style="color: #3daad6;">重点强调句。</strong></p>

<hr style="border: none; border-top: 1px solid #eee; margin: 2em 0;" />

<p style="margin: 1.5em 0; font-size: 18px; font-weight: bold; color: #2e6e9e;">章节标题</p>

<p style="margin: 1.5em 0;">新段落开始。</p>

<p style="margin: 1.5em 0; font-size: 13px; color: #a5a5a5;">注释说明文字</p>

</section>
```

## 工具推荐

- **浏览器排版**：秀米、简单易操作，需要Chrome浏览器
- **i排版**：小清新样式，有素材参考
- **壹伴**：有热文参考，样式种类多
- **新媒体管家**：比较稳定，服务内容多

## 关注引导

定制化，最好不要用现有的模板。

## 135编辑器

样式多，可以基于html5开发。
