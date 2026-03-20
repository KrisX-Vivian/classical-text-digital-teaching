import re
import json

def parse_questions(file_path):
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()

    # 分离题目区和答案区
    parts = content.split('参考答案与试题解析')
    if len(parts) != 2:
        raise ValueError('未找到参考答案分隔符')
    q_part = parts[0]
    a_part = '参考答案与试题解析' + parts[1]

    # 在题目区按题号分割（以“数字．”开头）
    q_blocks = re.split(r'\n(?=\d+．)', q_part.strip())
    # 去掉可能的第一行标题（如“一．选择题”）
    if q_blocks and not q_blocks[0][0].isdigit():
        q_blocks = q_blocks[1:]

    # 在答案区同样按题号分割
    a_blocks = re.split(r'\n(?=\d+．)', a_part.strip())
    if a_blocks and not a_blocks[0][0].isdigit():
        a_blocks = a_blocks[1:]

    questions = []
    for idx, q_block in enumerate(q_blocks):
        # 提取题号
        match = re.match(r'(\d+)．', q_block)
        if not match:
            continue
        num = match.group(1)

        # 题目内容（去除题号行开头的多余空白，保留原始格式）
        content_lines = q_block.splitlines()
        # 第一行是“题号．内容”，保留它，但去掉可能的前置空格
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

        # 在答案区找到对应题号的答案块
        if idx < len(a_blocks):
            a_block = a_blocks[idx]

            # 首先按 【解答】 分割，得到答案部分和解析部分
            parts_by_analysis = re.split(r'【解答】', a_block, maxsplit=1)
            if len(parts_by_analysis) == 2:
                answer_part = parts_by_analysis[0].strip()
                q['analysis'] = parts_by_analysis[1].strip()
            else:
                answer_part = a_block.strip()
                q['analysis'] = ''

            # 在 answer_part 中提取 【答案】 之后的内容作为真正的答案
            answer_match = re.search(r'【答案】\s*(.*?)(?=\n\d+．|\Z)', answer_part, re.S)
            if answer_match:
                q['answer'] = answer_match.group(1).strip()
            else:
                # 如果没有【答案】标记，则尝试直接取整个 answer_part（可能是简答题答案）
                # 但需要剔除可能重复的题号行
                lines = answer_part.splitlines()
                if lines:
                    # 如果第一行以题号开头，去掉第一行
                    if re.match(r'\d+．', lines[0]):
                        lines = lines[1:]
                q['answer'] = '\n'.join(lines).strip()

        questions.append(q)

    return questions

if __name__ == '__main__':
    import os
    script_dir = os.path.dirname(os.path.abspath(__file__))
    input_file = os.path.join(script_dir, '《红楼梦》情节考察题目合集.txt')
    output_file = os.path.join(script_dir, '情节考察.json')

    try:
        questions = parse_questions(input_file)
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(questions, f, ensure_ascii=False, indent=2)
        print(f'成功转换 {len(questions)} 道题目，已保存到 {output_file}')
        # 打印前两题作为示例
        print('\n示例：')
        for i, q in enumerate(questions[:2]):
            print(json.dumps(q, ensure_ascii=False, indent=2))
    except Exception as e:
        print(f'转换出错：{e}')