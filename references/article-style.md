# 公众号文章排版样式参考

## HTML 排版规范

### 外层容器

```html
<section style="font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, 'Helvetica Neue', Arial, sans-serif; padding: 20px; max-width: 100%;">
  <!-- 文章内容 -->
</section>
```

### 正文段落 `<p>`

```html
<p style="font-size: 16px; line-height: 2; color: #333; margin: 15px 0; text-align: justify;">
  文本内容
</p>
```

关键属性：
- `font-size: 16px` — 正文字号
- `line-height: 2` — 两倍行高，阅读舒适
- `color: #333` — 深灰色文字
- `margin: 15px 0` — 段间距
- `text-align: justify` — 两端对齐

### 短句换行

同一段落内的短句换行用 `<br />`，不要每个短句都开一个新 `<p>`：

```html
<p style="...">
  代码不会写？AI帮你写。<br />
  设计不会做？AI帮你做。<br />
  市场分析不会？AI帮你跑数据。
</p>
```

### 重点强调句

用 `<strong>` + 蓝色（`#1a73e8`）高亮关键观点：

```html
<strong style="color: #1a73e8;">这是重点内容</strong>
```

可以整段加粗：
```html
<p style="font-size: 16px; line-height: 2; color: #333; margin: 15px 0; text-align: justify;">
  <strong style="color: #1a73e8;">创新从来没有像今天这么容易。</strong>
</p>
```

也可以段内部分加粗：
```html
<p style="...">
  差距不在于谁的prompt写得更漂亮，<br />
  而在于<strong style="color: #1a73e8;">思维方式</strong>完全不同。
</p>
```

### 分隔线 `<hr>`

用于分隔文章的逻辑段落/章节：

```html
<hr style="border: none; border-top: 1px solid #eee; margin: 30px 0;" />
```

### 小标题 `<h2>`（可选）

如果文章有明确章节结构，使用 h2：

```html
<h2 style="font-size: 20px; font-weight: bold; color: #333; margin: 30px 0 15px 0; padding-bottom: 10px; border-bottom: 2px solid #1a73e8;">
  章节标题
</h2>
```

### 排版原则

1. **短句换行**：一行不超过 30 字左右，长句拆成短句用 `<br />` 换行
2. **段落留白**：每个 `<p>` 之间靠 `margin: 15px 0` 自然留白
3. **分隔线分段**：每 3-5 个段落之间插一条 `<hr />`，形成视觉节奏
4. **重点蓝色加粗**：每篇文章 3-6 处蓝色加粗，不宜过多
5. **不要用 `&nbsp;` 换行**：用 CSS margin 控制间距
6. **不用 markdown 格式**：全部使用内联 CSS 的 HTML

## 完整模板

```html
<section style="font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, 'Helvetica Neue', Arial, sans-serif; padding: 20px; max-width: 100%;">

<p style="font-size: 16px; line-height: 2; color: #333; margin: 15px 0; text-align: justify;">开头段落。</p>

<p style="font-size: 16px; line-height: 2; color: #333; margin: 15px 0; text-align: justify;">第二段。<br />短句换行。</p>

<p style="font-size: 16px; line-height: 2; color: #333; margin: 15px 0; text-align: justify;"><strong style="color: #1a73e8;">重点强调句。</strong></p>

<hr style="border: none; border-top: 1px solid #eee; margin: 30px 0;" />

<p style="font-size: 16px; line-height: 2; color: #333; margin: 15px 0; text-align: justify;">新段落开始。</p>

</section>
```
