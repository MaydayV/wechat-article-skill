# 公众号文章排版样式索引

## 简介

本目录下提供了多种公众号文章排版样式供选择。在配置文件 `wechat-article.config.json` 中通过 `writing.article_style` 字段指定。

## 可用排版样式

- **`default`**：OpenClaw 默认排版风格。
  - 文件路径：`references/styles/default.md`
  - 特点：标准的 16px 字号，2倍行高，两端对齐。

- **`gougestyle`**："狗哥排版"风格。
  - 文件路径：`references/styles/gougestyle.md`
  - 特点：15px 字号，1.75倍行高，左对齐，以及微信兼容性优化。适合长文阅读。

## 如何选择

在 `wechat-article.config.json` 中设置 `writing.article_style`：

```json
{
  "writing": {
    "article_style": "gougestyle" // 或者 "default"
  }
}
```

## 注意事项

- 不同排版样式可能对图片尺寸、颜色、行距有不同建议，请查阅具体样式文件。
- 最终 HTML 会根据所选样式进行渲染，并确保微信公众号兼容。
