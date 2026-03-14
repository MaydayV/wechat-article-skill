# 写作风格DNA（模板）

> 本文件由系统根据参考文章自动生成，用户可手动调整。
> 每次创作交互后系统会根据用户反馈自动更新。

## 基础特征

```yaml
sentence_avg_length: ""        # 例: "8-15字" / "20-40字"
paragraph_style: ""            # 例: "短段落，每段2-4句" / "长段落，每段5-8句"
rhythm: ""                     # 例: "快节奏，短句连击" / "舒缓，长短交替"
overall_tone: ""               # 例: "直接有力" / "温和理性" / "幽默轻松"
```

## 开头偏好

```yaml
preferred:
  - ""                         # 例: "场景代入" / "数字震撼" / "反问连击"
avoid:
  - ""                         # 例: "平铺直叙" / "今天我想聊聊..."
examples:
  - ""                         # 从参考文章中提取的开头示例
```

## 正文结构偏好

```yaml
section_style: ""              # 例: "无小标题，靠节奏推进" / "有明确小标题分段"
transition_style: ""           # 例: "话题跳跃但有暗线" / "逻辑递进" / "故事串联"
evidence_style: ""             # 例: "个人经历" / "数据引用" / "案例分析"
interaction_style: ""          # 例: "大量反问" / "设问自答" / "直接陈述"
```

## 金句偏好

```yaml
preferred_patterns:
  - ""                         # 例: "对比反转" / "短句定论" / "比喻类比"
avoid_patterns:
  - ""                         # 例: "排比三连" / "从来没有像今天这么..."
examples:
  - ""                         # 从参考文章中提取的金句示例
```

## 结尾偏好

```yaml
preferred:
  - ""                         # 例: "行动号召" / "金句收尾" / "开放式思考"
avoid:
  - ""                         # 例: "总结回顾" / "以上就是..."
examples:
  - ""                         # 从参考文章中提取的结尾示例
```

## 语言指纹

```yaml
favorite_phrases:
  - ""                         # 用户常用/喜欢的表达
avoid_phrases:
  - ""                         # 用户明确不喜欢的表达（如"赋能""闭环"）
punctuation_style: ""          # 例: "句号为主" / "省略号多" / "感叹号少"
person_perspective: ""         # 例: "第一人称" / "第三人称" / "混合"
```

## 主题风格映射

```yaml
# 不同主题类型使用不同的语言风格
money_topic:                   # 赚钱/变现类
  tone: ""                     # 例: "直接、数字、利益导向"
  keywords: []                 # 例: ["月入", "成本", "变现"]
tech_topic:                    # 技术/工具类
  tone: ""                     # 例: "具体、可操作、避坑"
  keywords: []
opinion_topic:                 # 观点/洞察类
  tone: ""                     # 例: "反常识、数据支撑"
  keywords: []
story_topic:                   # 故事/案例类
  tone: ""                     # 例: "画面感、冲突、情节"
  keywords: []
```

## 历史记录（系统自动维护）

```yaml
recent_articles: []            # 最近5篇文章标题
recent_openings: []            # 最近5篇使用的开头类型
recent_closings: []            # 最近5篇使用的结尾类型
recent_golden_phrases: []      # 最近使用过的金句（避免重复）
```

## 更新日志

- YYYY-MM-DD: 初始化，基于N篇参考文章生成
