import json

with open('hongloumeng_questions.json', 'r', encoding='utf-8') as f:
    data = json.load(f)

print("JSON格式验证通过!")
print(f"总题目数: {data['meta']['total']}")
print(f"选择题: {data['meta']['category_stats']['选择题']}")
print(f"分析题: {data['meta']['category_stats']['分析题']}")
print(f"简答题: {data['meta']['category_stats']['简答题']}")

print("\n前3题示例:")
for i, q in enumerate(data['questions'][:3], 1):
    print(f"\n{i}. ID: {q['id']}")
    print(f"   题型: {q['type']}")
    print(f"   题干: {q['question'][:80]}...")
    if q['options']:
        print(f"   选项: {q['options']}")
    print(f"   答案: {q['answer']}")
