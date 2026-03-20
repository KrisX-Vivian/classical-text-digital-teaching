import json
import re
import os

def normalize_text(text):
    if not text:
        return ""
    text = text.replace('\u3000', ' ').replace('\xa0', ' ')
    text = re.sub(r'\s+', ' ', text)
    return text.strip()

def clean_question_text(q_text):
    markers = [
        r'二[．\.]?名著导读',
        r'三[．\.]?现代文阅读',
        r'四[．\.]?语言文字应用',
        r'五[．\.]?作文',
        r'（共\d+小题）',
        r'第\d+题',
        r'第\d+小题',
        r'（共\d+题）',
        r'（共\d+小问）',
        r'（共\d+题）',
        r'一．', r'二．', r'三．', r'四．', r'五．',
        r'一\.', r'二\.', r'三\.', r'四\.', r'五\.'
    ]
    
    for marker in markers:
        q_text = re.sub(marker, '', q_text)
    
    q_text = re.sub(r'[A-D][．\.：:]\s*$', '', q_text)
    q_text = re.sub(r'\d+[\.．、]\s*$', '', q_text)
    q_text = normalize_text(q_text)
    
    return q_text.strip()

def extract_questions_from_file(filepath, filename):
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    answer_map = {}
    lines = content.split('\n')
    
    for i, line in enumerate(lines):
        line = line.strip()
        if '答案' in line and ('【' in line or '[' in line or '参考答案' in line):
            clean_line = re.sub(r'^[^\u4e00-\u9fa5A-D]*', '', line)
            clean_line = clean_line.replace('【答案】', '').replace('[答案]', '').replace('[参考答案]', '').replace('参考答案', '').replace('答案', '').strip()
            matches = re.findall(r'(?:^|[^\u4e00-\u9fa5])([A-D])(?:[\s　。，,]|$)', clean_line)
            for j, m in enumerate(matches):
                if j + 1 not in answer_map:
                    answer_map[j + 1] = m

    questions = []
    question_blocks = re.split(r'\n(?=\d+[.．、])', content)

    for block in question_blocks:
        if not block.strip():
            continue
        
        if '答案' in block[:100] and '【' in block[:100]:
            continue

        q_match = re.match(r'^(\d+)[.．、]\s*(.+?)$', block, re.DOTALL)
        if not q_match:
            continue

        q_num = int(q_match.group(1))
        q_text = q_match.group(2).strip()

        q_text = clean_question_text(q_text)

        if len(q_text) < 8:
            continue

        options = []
        option_lines = re.findall(r'^([A-D])[.．:：]\s*(.+)$', block, re.MULTILINE)
        for opt in option_lines:
            opt_text = normalize_text(opt[1])
            opt_text = re.sub(r'^[A-D][.．:：]\s*', '', opt_text)
            if len(opt_text) > 2:
                options.append(f"{opt[0]}. {opt_text}")

        if len(options) >= 2:
            q_type = '选择题'
        elif '分析' in q_text or '请结合' in q_text or '请谈谈' in q_text or '请简析' in q_text or '论述' in q_text:
            q_type = '分析题'
        else:
            q_type = '简答题'

        answer = answer_map.get(q_num, None)

        questions.append({
            'question': q_text[:800],
            'options': options if options else None,
            'type': q_type,
            'answer': answer,
            'source': filename
        })

    return questions

def main():
    base_path = r'd:\大创项目\classical-literature-ai-web\data\红楼梦题库--txt版本'

    files = [
        '《红楼梦》情节考察题目合集.txt',
        '《红楼梦》人物形象考察题目合集.txt',
        '《红楼梦》与其他领域（表演、戏曲等）结合题目合集.txt',
        '《红楼梦》与诗词有关题目合集.txt',
        '《红楼梦》阅读理解类题目合集.txt'
    ]

    all_questions = []
    file_stats = {}

    for filename in files:
        filepath = os.path.join(base_path, filename)
        questions = extract_questions_from_file(filepath, filename)
        
        file_stats[filename] = len(questions)
        all_questions.extend(questions)

    print("=" * 60)
    print("文件题目统计:")
    for f, count in file_stats.items():
        print(f"  {f}: {count}题")
    print(f"\n提取总题数: {len(all_questions)}")

    seen_questions = {}
    unique_questions = []
    duplicates_count = 0
    
    for q in all_questions:
        q_key = normalize_text(q['question'])
        if q_key in seen_questions:
            duplicates_count += 1
            continue
        seen_questions[q_key] = True
        unique_questions.append(q)

    print(f"\n去重后题数: {len(unique_questions)}")
    print(f"重复题目数: {duplicates_count}")

    choice_count = sum(1 for q in unique_questions if q['type'] == '选择题')
    analysis_count = sum(1 for q in unique_questions if q['type'] == '分析题')
    short_count = sum(1 for q in unique_questions if q['type'] == '简答题')

    print(f"\n题型分布:")
    print(f"  选择题: {choice_count}")
    print(f"  分析题: {analysis_count}")
    print(f"  简答题: {short_count}")

    final_questions = []
    for i, q in enumerate(unique_questions, 1):
        final_questions.append({
            'id': f'hrm-{str(i).zfill(3)}',
            'type': q['type'],
            'question': q['question'],
            'options': q['options'],
            'answer': q['answer']
        })

    output_data = {
        'meta': {
            'title': '《红楼梦》题库完整合集',
            'source_files': list(file_stats.keys()),
            'total': len(final_questions),
            'category_stats': {
                '选择题': choice_count,
                '分析题': analysis_count,
                '简答题': short_count
            },
            'generated_at': '2026-03-09',
            'processing_notes': [
                f'从5个TXT文件提取题目',
                f'提取总题目: {len(all_questions)}',
                f'去重后题目: {len(unique_questions)}',
                f'重复题目: {duplicates_count}',
                '题型只分三类：选择题、简答题、分析题',
                '已清理题目中的杂质内容'
            ]
        },
        'questions': final_questions
    }

    output_path = os.path.join(base_path, 'hongloumeng_questions.json')
    with open(output_path, 'w', encoding='utf-8') as f:
        json.dump(output_data, f, ensure_ascii=False, indent=2)

    print(f"\n已保存到: {output_path}")
    print("\n前5题预览:")
    for i, q in enumerate(final_questions[:5], 1):
        print(f"{i}. [{q['type']}] {q['question'][:50]}...")
        if q['options']:
            print(f"   选项数: {len(q['options'])}, 答案: {q['answer']}")

if __name__ == "__main__":
    main()
