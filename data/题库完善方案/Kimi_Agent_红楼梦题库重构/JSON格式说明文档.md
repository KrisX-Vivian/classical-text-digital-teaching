# 《红楼梦》题库JSON格式说明 (v2.1)

## 📋 文件说明

本JSON文件采用标准化结构设计，便于前端展示和后续扩展。

---

## 🏗️ 整体结构

```json
{
  "metadata": { ... },      // 元数据信息
  "questions": [ ... ]      // 题目数组
}
```

---

## 📄 题目结构详解

### 通用字段（所有题型）

| 字段 | 类型 | 说明 | 示例 |
|------|------|------|------|
| `id` | string | 唯一标识符 | "hrm-001" |
| `category.primary` | string | 一级分类（知识维度） | "人物形象" |
| `category.secondary` | string | 二级分类 | ""（可留空） |
| `type` | string | 题型代码 | "single_choice" |
| `difficulty` | string | 难度等级 | "easy"/"medium"/"hard" |
| `source` | string | 题目来源 | "《红楼梦》题库合集" |
| `tags` | array | 标签数组 | ["宝玉", "黛玉葬花"] |
| `statistics.correctRate` | number/null | 正确率 | null（待补充） |
| `statistics.attempts` | number | 作答次数 | 0 |

---

## 📝 各题型详细结构

### 1. 单选题 (single_choice)

```json
{
  "id": "hrm-001",
  "category": { "primary": "情节考察", "secondary": "" },
  "type": "single_choice",
  "difficulty": "medium",
  "content": {
    "stem": "下列文学常识的表述，不正确的一项是（ ）",
    "options": [
      { "label": "A", "text": "选项A的内容..." },
      { "label": "B", "text": "选项B的内容..." },
      { "label": "C", "text": "选项C的内容..." },
      { "label": "D", "text": "选项D的内容..." }
    ]
  },
  "answer": {
    "correct": "A",
    "analysis": "解析内容...",
    "keyPoints": ["考点1", "考点2"]
  }
}
```

**前端渲染示例：**

```vue
<template>
  <div class="single-choice">
    <p class="stem">{{ question.content.stem }}</p>
    <div class="options">
      <div v-for="opt in question.content.options" :key="opt.label" class="option">
        <span class="label">{{ opt.label }}.</span>
        <span class="text">{{ opt.text }}</span>
      </div>
    </div>
  </div>
</template>
```

---

### 2. 多选题 (multiple_choice)

结构与单选题相同，`answer.correct` 为数组：

```json
"answer": {
  "correct": ["A", "C"],
  "analysis": "..."
}
```

---

### 3. 填空题 (fill_blank)

```json
{
  "type": "fill_blank",
  "content": {
    "stem": "《红楼梦》的作者是______，字______。"
  },
  "answer": {
    "correct": "曹雪芹|梦阮",
    "analysis": "..."
  }
}
```

---

### 4. 简答题 (short_answer)

```json
{
  "type": "short_answer",
  "content": {
    "stem": "简述贾宝玉的性格特点。"
  },
  "answer": {
    "correct": "贾宝玉性格叛逆，厌恶科举...",
    "analysis": "...",
    "keyPoints": ["叛逆性格", "厌恶科举", "尊重女性"]
  }
}
```

---

### 5. 分析题 (analysis)

```json
{
  "type": "analysis",
  "content": {
    "stem": "结合具体情节，分析林黛玉的人物形象。"
  },
  "answer": {
    "correct": "林黛玉是《红楼梦》中的主要人物...",
    "analysis": "...",
    "keyPoints": ["敏感多疑", "才华横溢", "悲剧命运"]
  }
}
```

---

### 6. 作文题 (essay)

```json
{
  "type": "essay",
  "content": {
    "stem": "阅读下面的材料，根据要求写作。\n\n材料内容...",
    "wordLimit": 800
  },
  "answer": {
    "correct": "参考范文...",
    "analysis": "立意要点...",
    "keyPoints": ["审题", "立意", "结构", "语言"]
  }
}
```

---

### 7. 复合题 (composite) ⭐重点

复合题包含**阅读材料**和**多个子题目**：

```json
{
  "type": "composite",
  "content": {
    "material": "阅读材料（长文本）...",
    "mainStem": "阅读上述材料，完成下列各题。",
    "subQuestions": [
      {
        "id": "sub-1",
        "order": 1,
        "type": "single_choice",
        "stem": "小题1的题干",
        "options": [ ... ]
      },
      {
        "id": "sub-2", 
        "order": 2,
        "type": "fill_blank",
        "stem": "小题2的题干"
      },
      {
        "id": "sub-3",
        "order": 3,
        "type": "analysis",
        "stem": "小题3的题干"
      }
    ]
  }
}
```

**前端渲染示例：**

```vue
<template>
  <div class="composite-question">
    <!-- 阅读材料 -->
    <div class="material" v-if="question.content.material">
      <h4>阅读材料</h4>
      <pre>{{ question.content.material }}</pre>
    </div>

    <!-- 引导语 -->
    <p class="main-stem">{{ question.content.mainStem }}</p>

    <!-- 子题目 -->
    <div class="sub-questions">
      <div v-for="sub in question.content.subQuestions" :key="sub.id" class="sub-question">
        <span class="order">({{ sub.order }})</span>
        <component :is="getComponentType(sub.type)" :question="sub" />
      </div>
    </div>
  </div>
</template>
```

---

### 8. 语言表达 (language_expr)

```json
{
  "type": "language_expr",
  "content": {
    "stem": "请用100字左右描述...",
    "format": "微写作",
    "maxLength": 150
  }
}
```

---

## 🔧 题型代码对照表

| 代码 | 中文名称 | 说明 |
|------|----------|------|
| `single_choice` | 单选题 | 4选1 |
| `multiple_choice` | 多选题 | 多选多 |
| `fill_blank` | 填空题 | 默写/填空 |
| `short_answer` | 简答题 | 简要回答 |
| `analysis` | 分析题 | 深度分析 |
| `essay` | 作文题 | 材料作文 |
| `composite` | 复合题 | 阅读+多小题 |
| `language_expr` | 语言表达 | 微写作 |

---

## 📊 难度等级

| 代码 | 中文 | 说明 |
|------|------|------|
| `easy` | 易 | 基础知识点 |
| `medium` | 中 | 需要理解分析 |
| `hard` | 难 | 需要综合运用 |

---

## 🏷️ 知识分类

| 一级分类 | 说明 |
|----------|------|
| `情节考察` | 经典场景、情节顺序、细节记忆 |
| `人物形象` | 主要人物、次要人物、人物关系 |
| `诗词鉴赏` | 诗词默写、赏析、创作背景 |
| `阅读理解` | 现代文阅读、诗歌阅读 |
| `跨领域结合` | 戏曲、建筑、绘画等 |

---

## ✅ 答案字段说明

所有题型的答案都包含以下字段：

| 字段 | 类型 | 说明 |
|------|------|------|
| `answer.correct` | string/array | 正确答案 |
| `answer.analysis` | string | 详细解析 |
| `answer.keyPoints` | array | 评分要点 |

**注意：** 如果题目暂时没有答案，这些字段会为空字符串或空数组，后续可以补充或使用AI模型生成。

---

## 🚀 快速开始代码

### 1. 加载JSON

```javascript
const fs = require('fs');
const data = JSON.parse(fs.readFileSync('hongloumeng_questions_v2.1.json', 'utf8'));

console.log(`共加载 ${data.metadata.statistics.totalQuestions} 道题目`);
```

### 2. 按分类筛选

```javascript
// 筛选人物形象类的分析题
const filtered = data.questions.filter(q => 
  q.category.primary === '人物形象' && 
  q.type === 'analysis'
);
```

### 3. 按题型筛选

```javascript
// 获取所有选择题
const choices = data.questions.filter(q => 
  ['single_choice', 'multiple_choice'].includes(q.type)
);
```

### 4. 获取复合题

```javascript
const composites = data.questions.filter(q => q.type === 'composite');

// 统计子题目数量
const totalSubQuestions = composites.reduce((sum, q) => 
  sum + q.content.subQuestions.length, 0
);
```

---

## 🛡️ 数据质量保证

### 已完成的验证

- ✅ 所有选择题选项已正确分离
- ✅ 题目文本已清理多余空白
- ✅ 段落结构已保持
- ✅ ID唯一性检查通过
- ✅ 必填字段检查通过

### 建议的验证流程

```javascript
function validateQuestion(q) {
  const errors = [];

  // 必填字段
  ['id', 'category', 'type', 'content'].forEach(field => {
    if (!q[field]) errors.push(`缺少字段: ${field}`);
  });

  // 选择题验证
  if (['single_choice', 'multiple_choice'].includes(q.type)) {
    const opts = q.content.options;
    if (!opts || opts.length < 2) {
      errors.push('选择题至少需要2个选项');
    }
    // 验证选项格式
    opts.forEach((opt, i) => {
      if (!opt.label || !opt.text) {
        errors.push(`选项${i+1}格式不正确`);
      }
    });
  }

  return errors;
}
```

---

## 📈 版本历史

| 版本 | 日期 | 变更 |
|------|------|------|
| 2.1 | 2026-03-10 | 优化选择题格式，分离选项 |
| 2.0 | 2026-03-10 | 重构分类体系，添加复合题型 |
| 1.0 | 2026-03-09 | 初始版本 |

---

## 💡 常见问题

### Q1: 答案为空怎么办？

A: 可以：
1. 后续人工补充
2. 使用AI模型（如GPT）生成答案和解析
3. 前端展示时显示"答案待补充"

### Q2: 如何添加新题目？

A: 按照上述格式添加即可，注意：
- ID保持唯一
- 使用正确的题型代码
- 选择题选项使用 `{label, text}` 格式

### Q3: 复合题的子题目如何计分？

A: 建议：
- 每道子题独立计分
- 大题总分 = 子题分数之和
- 可以设置子题权重

---

*文档版本: v2.1*
*更新日期: 2026-03-10*
