# 《红楼梦》题库JSON格式说明 (v2.3)

## 📋 文件说明

本JSON文件采用标准化结构设计，便于前端展示和后续扩展。

**版本**: v2.3  
**更新日期**: 2026-03-10  
**总题目数**: 99道  
**复合题数**: 55道

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
| `id` | string | 唯一标识符 | "hrm-008" |
| `category.primary` | string | 一级分类（知识维度） | "人物形象" |
| `category.secondary` | string | 二级分类 | ""（可留空） |
| `type` | string | 题型代码 | "composite" |
| `difficulty` | string | 难度等级 | "easy"/"medium"/"hard" |
| `source` | string | 题目来源 | "《红楼梦》题库合集" |
| `tags` | array | 标签数组 | ["宝玉", "黛玉葬花"] |
| `statistics.correctRate` | number/null | 正确率 | null |
| `statistics.attempts` | number | 作答次数 | 0 |

---

## 📝 各题型详细结构

### 1. 单选题 (single_choice)

```json
{
  "id": "hrm-001",
  "type": "single_choice",
  "content": {
    "stem": "下列文学常识的表述，不正确的一项是（ ）",
    "options": [
      { "label": "A", "text": "选项A内容..." },
      { "label": "B", "text": "选项B内容..." },
      { "label": "C", "text": "选项C内容..." },
      { "label": "D", "text": "选项D内容..." }
    ]
  },
  "answer": {
    "correct": "A",
    "analysis": "解析内容...",
    "keyPoints": []
  }
}
```

---

### 2. 复合题 (composite) ⭐重点

复合题包含**阅读材料**和**多个子题目**，子题目可以是不同题型：

```json
{
  "id": "hrm-008",
  "type": "composite",
  "content": {
    "material": "《红楼梦》第三十三回：宝玉急的跺脚...",
    "stem": "根据要求，回答问题。",
    "subQuestions": [
      {
        "id": "sub-1",
        "order": 1,
        "type": "fill_blank",
        "stem": "'手足'指的是（人名）",
        "options": null
      },
      {
        "id": "sub-2",
        "order": 2,
        "type": "analysis",
        "stem": "对'不肖'之举的具体内容加以解说",
        "options": null
      },
      {
        "id": "sub-3",
        "order": 3,
        "type": "single_choice",
        "stem": "下列表述与原著内容相符合的一项是",
        "options": [
          { "label": "A", "text": "..." },
          { "label": "B", "text": "..." },
          { "label": "C", "text": "..." },
          { "label": "D", "text": "..." }
        ]
      }
    ]
  }
}
```

**子题目题型说明**:

| 类型 | 说明 |
|------|------|
| `single_choice` | 单选题（有options） |
| `fill_blank` | 填空题 |
| `short_answer` | 简答题 |
| `analysis` | 分析题 |

---

### 3. 分析题 (analysis)

```json
{
  "type": "analysis",
  "content": {
    "material": "阅读材料...",      // 可选
    "stem": "结合材料分析问题..."
  },
  "answer": {
    "correct": "答案...",
    "analysis": "解析...",
    "keyPoints": ["要点1", "要点2"]
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
    "correct": "贾宝玉性格叛逆...",
    "analysis": "...",
    "keyPoints": ["叛逆性格", "厌恶科举", "尊重女性"]
  }
}
```

---

### 5. 填空题 (fill_blank)

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

## 🚀 前端渲染示例

### 复合题渲染

```vue
<template>
  <div class="composite-question">
    <!-- 阅读材料 -->
    <div v-if="question.content.material" class="material-section">
      <h4>阅读材料</h4>
      <div class="material-content">{{ question.content.material }}</div>
    </div>

    <!-- 引导语 -->
    <p class="main-stem">{{ question.content.stem }}</p>

    <!-- 子题目 -->
    <div class="sub-questions">
      <div 
        v-for="sub in question.content.subQuestions" 
        :key="sub.id"
        class="sub-question"
      >
        <span class="order">({{ sub.order }})</span>

        <!-- 单选题 -->
        <div v-if="sub.type === 'single_choice'" class="single-choice">
          <p class="stem">{{ sub.stem }}</p>
          <div class="options">
            <div v-for="opt in sub.options" :key="opt.label" class="option">
              <span class="label">{{ opt.label }}.</span>
              <span class="text">{{ opt.text }}</span>
            </div>
          </div>
        </div>

        <!-- 填空题 -->
        <div v-else-if="sub.type === 'fill_blank'" class="fill-blank">
          <p class="stem">{{ sub.stem }}</p>
          <input type="text" placeholder="请输入答案" />
        </div>

        <!-- 简答题/分析题 -->
        <div v-else class="text-answer">
          <p class="stem">{{ sub.stem }}</p>
          <textarea placeholder="请输入答案"></textarea>
        </div>
      </div>
    </div>
  </div>
</template>
```

---

## ✅ 答案字段说明

所有题型的答案都包含以下字段：

| 字段 | 类型 | 说明 |
|------|------|------|
| `answer.correct` | string/array | 正确答案 |
| `answer.analysis` | string | 详细解析 |
| `answer.keyPoints` | array | 评分要点 |

**注意**: 如果题目暂时没有答案，这些字段会为空字符串或空数组，后续可以补充或使用AI模型生成。

---

## 💡 答案处理方案

### 方案1: 预留空字段（当前做法）

```json
"answer": {
  "correct": "",
  "analysis": "",
  "keyPoints": []
}
```

前端判断：
```javascript
const hasAnswer = question.answer.correct && question.answer.correct.length > 0;
```

### 方案2: AI生成答案

```javascript
async function generateAnswerWithAI(question) {
  const prompt = `请为以下题目生成答案和解析：\n\n题目：${question.content.stem}`;

  const response = await fetch('/api/ai/answer', {
    method: 'POST',
    body: JSON.stringify({ question })
  });

  return response.json();
}
```

---

## 📈 版本历史

| 版本 | 日期 | 变更 |
|------|------|------|
| 2.3 | 2026-03-10 | 修复复合题解析，正确分离子题目 |
| 2.2 | 2026-03-10 | 优化选择题格式，分离选项 |
| 2.1 | 2026-03-10 | 清理文本格式 |
| 2.0 | 2026-03-10 | 重构分类体系 |
| 1.0 | 2026-03-09 | 初始版本 |

---

*文档版本: v2.3*  
*更新日期: 2026-03-10*
