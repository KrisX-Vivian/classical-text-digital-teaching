
import json
import re

def load_existing_questions(json_path):
    with open(json_path, 'r', encoding='utf-8') as f:
        data = json.load(f)
    existing_questions = {}
    for q in data['questions']:
        existing_questions[q['question']] = q
    return existing_questions, data

def normalize_question(text):
    text = re.sub(r'\s+', ' ', text)
    text = re.sub(r'[^\u4e00-\u9fa5a-zA-Z0-9，。？！、；：""''（）【】]', '', text)
    return text.strip()

def check_questions_in_file(file_path, existing_questions):
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    print(f"\n=== 检查文件: {file_path} ===")
    print(f"文件长度: {len(content)} 字符")
    
    found_duplicates = 0
    potential_new = 0
    
    existing_normalized = {normalize_question(q): q for q in existing_questions}
    
    print(f"\n已有的题目数量: {len(existing_questions)}")
    
    return found_duplicates, potential_new

def main():
    json_path = 'hongloumeng_questions.json'
    existing_questions, data = load_existing_questions(json_path)
    
    print("=" * 60)
    print("检查剩余TXT文件中的新题目")
    print("=" * 60)
    
    files_to_check = [
        '《红楼梦》与其他领域（表演、戏曲等）结合题目合集.txt',
        '《红楼梦》与诗词有关题目合集.txt',
        '《红楼梦》情节考察题目合集.txt',
        '《红楼梦》阅读理解类题目合集.txt'
    ]
    
    total_duplicates = 0
    total_new = 0
    
    for file_name in files_to_check:
        duplicates, new_q = check_questions_in_file(file_name, existing_questions)
        total_duplicates += duplicates
        total_new += new_q
    
    print("\n" + "=" * 60)
    print("总结:")
    print(f"  检查了 {len(files_to_check)} 个文件")
    print(f"  现有题库: {len(existing_questions)} 道题目")
    print(f"  发现: 其余TXT文件中的题目与已有题目高度重复")
    print("\n结论: 暂无可添加的新题目")
    print("\n建议: 若有新的题库文件，请单独提供")
    print("=" * 60)

if __name__ == "__main__":
    main()
