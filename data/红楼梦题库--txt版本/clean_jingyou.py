import json
import re

input_file = r'd:\大创项目\classical-literature-ai-web\data\红楼梦题库--txt版本\questions.json'
output_file = r'd:\大创项目\classical-literature-ai-web\data\红楼梦题库--txt版本\questions_cleaned.json'

with open(input_file, 'r', encoding='utf-8') as f:
    data = json.load(f)

def clean_text(text):
    if not text:
        return text
    pattern = r'声明：试题解析著作权属菁优网所有.*?菁优网小程序'
    return re.sub(pattern, '', text, flags=re.DOTALL).strip()

cleaned_data = []
for q in data:
    q['analysis'] = clean_text(q.get('analysis', ''))
    q['answer'] = clean_text(q.get('answer', ''))
    q['content'] = clean_text(q.get('content', ''))
    cleaned_data.append(q)

with open(output_file, 'w', encoding='utf-8') as f:
    json.dump(cleaned_data, f, ensure_ascii=False, indent=2)

print(f'已清理完成！输出文件：{output_file}')
print('请将 questions_cleaned.json 重命名为 questions.json 替换原文件')