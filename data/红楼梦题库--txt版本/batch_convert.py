import re
import json
from pathlib import Path

# 文件名到分类的映射规则（可根据实际文件名调整）
CATEGORY_MAP = {
    '情节考察': '情节考察',
    '人物形象': '人物形象',
    '诗词': '诗词鉴赏',
    '阅读理解': '阅读理解',
    '与其他领域结合': '跨领域结合'
}

def parse_questions(file_path):
    """解析单个文件，返回题目列表"""
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()

    # 分离题目区和答案区
    parts = content.split('参考答案与试题解析')
    if len(parts) != 2:
        print(f'警告：文件 {file_path.name} 未找到参考答案分隔符，跳过')
        return []
    q_part = parts[0]
    a_part = '参考答案与试题解析' + parts[1]

    # 在题目区按题号分割（以“数字．”开头）
    q_blocks = re.split(r'\n(?=\d+．)', q_part.strip())
    if q_blocks and not q_blocks[0][0].isdigit():
        q_blocks = q_blocks[1:]

    # 在答案区同样按题号分割
    a_blocks = re.split(r'\n(?=\d+．)', a_part.strip())
    if a_blocks and not a_blocks[0][0].isdigit():
        a_blocks = a_blocks[1:]

    questions = []
    for idx, q_block in enumerate(q_blocks):
        match = re.match(r'(\d+)．', q_block)
        if not match:
            continue
        num = match.group(1)

        # 题目内容
        content_lines = q_block.splitlines()
        title_line = content_lines[0].lstrip()
        rest = '\n'.join(content_lines[1:]).strip()
        full_content = title_line + ('\n' + rest if rest else '')

        q = {
            "id": idx + 1,
            "title": f"第{num}题",
            "content": full_content,
            "answer": "",
            "analysis": ""
        }

        # 匹配答案
        if idx < len(a_blocks):
            a_block = a_blocks[idx]

            # 按 【解答】 分割
            parts_by_analysis = re.split(r'【解答】', a_block, maxsplit=1)
            if len(parts_by_analysis) == 2:
                answer_part = parts_by_analysis[0].strip()
                q['analysis'] = parts_by_analysis[1].strip()
            else:
                answer_part = a_block.strip()
                q['analysis'] = ''

            # 提取 【答案】 之后的内容
            answer_match = re.search(r'【答案】\s*(.*?)(?=\n\d+．|\Z)', answer_part, re.S)
            if answer_match:
                q['answer'] = answer_match.group(1).strip()
            else:
                # 没有【答案】标记时，尝试去掉题号行后作为答案
                lines = answer_part.splitlines()
                if lines and re.match(r'\d+．', lines[0]):
                    lines = lines[1:]
                q['answer'] = '\n'.join(lines).strip()

        questions.append(q)
    return questions

def detect_category(file_name):
    """根据文件名猜测分类"""
    name = file_name.stem
    for key, cat in CATEGORY_MAP.items():
        if key in name:
            return cat
    return '其他'  # 未知分类

def main():
    base_dir = Path(__file__).resolve().parent
    # 匹配所有可能的txt文件（可根据实际需要调整模式）
    txt_files = list(base_dir.glob('《红楼梦》*.txt'))
    if not txt_files:
        print('未找到任何《红楼梦》相关的txt文件')
        return

    for file_path in txt_files:
        print(f'正在处理：{file_path.name}')
        questions = parse_questions(file_path)
        if not questions:
            print(f'  文件 {file_path.name} 未解析到题目，跳过')
            continue

        # 确定分类
        category = detect_category(file_path)
        # 为每个题目添加分类字段（可选，方便前端使用）
        for q in questions:
            q['category'] = category

        output_file = base_dir / f'{category}.json'
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(questions, f, ensure_ascii=False, indent=2)
        print(f'  成功转换 {len(questions)} 道题目，已保存到 {output_file.name}')

if __name__ == '__main__':
    main()