import json
import os

def generate_question_html(question_data, index):
    q_id = question_data['id']
    q_type = question_data['type']
    question = question_data['question']
    options = question_data.get('options', None)
    answer = question_data.get('answer', None)
    
    type_map = {
        '选择题': 'choice',
        '简答题': 'short',
        '分析题': 'analysis'
    }
    html_type = type_map.get(q_type, 'short')
    
    html_parts = []
    html_parts.append(f'<div class="exercise-card delay-{((index % 5) + 1)}" data-type="{html_type}">')
    
    keyword = '《红楼梦》'
    if keyword in question:
        question = question.replace(keyword, f'<span class="keyword">{keyword}</span>')
    
    html_parts.append(f'    <h3>{question}</h3>')
    html_parts.append(f'    <div class="difficulty-stars">★★☆</div>')
    
    type_tags = {
        '选择题': '<span class="text-type-tag"><i class="bi bi-list-check"></i> 选择题</span>',
        '简答题': '<span class="text-type-tag"><i class="bi bi-pencil-square"></i> 简答题</span>',
        '分析题': '<span class="text-type-tag"><i class="bi bi-journal-text"></i> 分析题</span>'
    }
    html_parts.append(f'    {type_tags.get(q_type, type_tags["简答题"])}')
    
    if q_type == '选择题' and options:
        html_parts.append('    <p class="exercise-content">请从以下选项中选择正确答案：</p>')
        html_parts.append('    <div class="exercise-options mb-3">')
        for i, opt in enumerate(options):
            label_id = f'{q_id}-opt{i}'
            html_parts.append(f'        <div class="form-check">')
            html_parts.append(f'            <input class="form-check-input" type="radio" name="{q_id}" id="{label_id}">')
            html_parts.append(f'            <label class="form-check-label" for="{label_id}">{opt}</label>')
            html_parts.append(f'        </div>')
        html_parts.append('    </div>')
    else:
        html_parts.append('    <p class="exercise-content">请简述你的理解：</p>')
        html_parts.append('    <textarea class="form-control mb-3" rows="4" placeholder="请输入你的答案..."></textarea>')
    
    answer_id = f'{q_id}-answer'
    html_parts.append(f'    <button class="guofeng-btn" type="button" data-bs-toggle="collapse" data-bs-target="#{answer_id}">')
    html_parts.append(f'        <i class="bi bi-eye"></i> 查看答案/解析')
    html_parts.append(f'    </button>')
    
    html_parts.append(f'    <div class="collapse mt-3" id="{answer_id}">')
    html_parts.append(f'        <div class="answer-card">')
    if answer:
        html_parts.append(f'            <p><strong class="correct-answer">答案：</strong>{answer}</p>')
    html_parts.append(f'            <p><strong>解析：</strong>请参考《红楼梦》原著相关内容进行解析。</p>')
    html_parts.append(f'        </div>')
    html_parts.append(f'    </div>')
    
    html_parts.append('</div>')
    return '\n'.join(html_parts)

def main():
    json_path = r'd:\大创项目\classical-literature-ai-web\data\红楼梦题库--txt版本\hongloumeng_questions.json'
    html_path = r'd:\大创项目\classical-literature-ai-web\exercises.html'
    
    with open(json_path, 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    questions = data['questions']
    
    print(f'共读取 {len(questions)} 道题目')
    
    html_parts = []
    for i, q in enumerate(questions, 1):
        html_parts.append(generate_question_html(q, i))
    
    all_questions_html = '\n\n'.join(html_parts)
    
    with open(html_path, 'r', encoding='utf-8') as f:
        html_content = f.read()
    
    start_marker = '<!-- 选择题卡片 -->'
    end_marker = '<!-- 互动小游戏模块 -->'
    
    start_idx = html_content.find(start_marker)
    end_idx = html_content.find(end_marker)
    
    if start_idx != -1 and end_idx != -1:
        new_html = (
            html_content[:start_idx + len(start_marker)] + '\n\n' +
            all_questions_html + '\n\n' +
            html_content[end_idx:]
        )
        
        with open(html_path, 'w', encoding='utf-8') as f:
            f.write(new_html)
        
        print(f'成功更新 {html_path}')
        print(f'插入了 {len(questions)} 道题目')
    else:
        print('未找到标记位置')

if __name__ == '__main__':
    main()
