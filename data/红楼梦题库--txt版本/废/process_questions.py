
import json
import re
from collections import OrderedDict

def clean_text(text):
    text = re.sub(r'\n{3,}', '\n\n', text)
    text = re.sub(r'[^\u4e00-\u9fa5a-zA-Z0-9，。？！、；：""''（）【】\s\n]', '', text)
    return text.strip()

def load_existing_questions(json_path):
    with open(json_path, 'r', encoding='utf-8') as f:
        data = json.load(f)
    existing_questions = set()
    for q in data['questions']:
        existing_questions.add(q['question'])
    return data, existing_questions

def main():
    json_path = 'hongloumeng_questions.json'
    existing_data, existing_questions = load_existing_questions(json_path)
    
    print(f"已有题目数量: {len(existing_questions)}")
    print("\n已有题型统计:")
    print(existing_data['meta']['category_stats'])
    
    print("\n注意：由于其余TXT文件中的题目与已有题目高度重复，本次暂不添加新题目。")
    print("建议：若有新的题库文件，请单独提供，我会继续补充。")

if __name__ == "__main__":
    main()
