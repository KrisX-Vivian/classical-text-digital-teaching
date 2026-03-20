import json
import os

def convert_to_legacy_format(new_data):
    type_map = {
        'single_choice': '选择题',
        'short_answer': '简答题', 
        'analysis': '分析题',
        'composite': '简答题',
        'essay': '简答题',
        'language_expr': '简答题'
    }
    
    legacy_questions = []
    
    for q in new_data['questions']:
        question_text = ''
        options = None
        
        if q['type'] == 'composite' and q.get('content', {}).get('subQuestions'):
            parts = []
            if q.get('content', {}).get('material'):
                parts.append(q['content']['material'])
            if q.get('content', {}).get('mainStem'):
                parts.append(q['content']['mainStem'])
            
            for sub in q['content']['subQuestions']:
                parts.append(sub['stem'])
            
            question_text = '\n\n'.join(parts)
        elif q.get('content', {}).get('stem'):
            question_text = q['content']['stem']
            if q.get('content', {}).get('material'):
                question_text = q['content']['material'] + '\n\n' + question_text
        
        if q['type'] == 'single_choice' and q.get('content', {}).get('options'):
            options = [f"{opt['label']}. {opt['text']}" for opt in q['content']['options']]
        
        answer = None
        if q.get('answer', {}).get('correct'):
            answer = q['answer']['correct']
        
        legacy_questions.append({
            'id': q['id'],
            'type': type_map.get(q['type'], '简答题'),
            'question': question_text.strip(),
            'options': options,
            'answer': answer
        })
    
    return {
        'meta': {
            'title': new_data['metadata']['title'],
            'source_files': new_data['metadata']['sourceFiles'],
            'total': new_data['metadata']['statistics']['totalQuestions'],
            'category_stats': {
                '选择题': new_data['metadata']['statistics']['typeDistribution'].get('single_choice', 0),
                '分析题': new_data['metadata']['statistics']['typeDistribution'].get('analysis', 0),
                '简答题': sum([
                    new_data['metadata']['statistics']['typeDistribution'].get('short_answer', 0),
                    new_data['metadata']['statistics']['typeDistribution'].get('composite', 0),
                    new_data['metadata']['statistics']['typeDistribution'].get('essay', 0),
                    new_data['metadata']['statistics']['typeDistribution'].get('language_expr', 0)
                ])
            },
            'generated_at': new_data['metadata']['lastUpdated'],
            'processing_notes': [
                '从新版v2.4 JSON转换而来',
                f'保留题目总数: {len(legacy_questions)}',
                '题型映射：single_choice→选择题，其他→简答题/分析题',
                '复合题型已合并为单个题目'
            ]
        },
        'questions': legacy_questions
    }

def main():
    new_path = r'd:\大创项目\classical-literature-ai-web\data\题库完善方案\Kimi_Agent_红楼梦题库重构\hongloumeng_questions_v2.4.json'
    output_path = r'd:\大创项目\classical-literature-ai-web\data\红楼梦题库--txt版本\hongloumeng_questions_v2.4_legacy.json'
    
    with open(new_path, 'r', encoding='utf-8') as f:
        new_data = json.load(f)
    
    legacy_data = convert_to_legacy_format(new_data)
    
    with open(output_path, 'w', encoding='utf-8') as f:
        json.dump(legacy_data, f, ensure_ascii=False, indent=2)
    
    print(f'转换完成！')
    print(f'题目总数: {len(legacy_data["questions"])}')
    print(f'选择题: {legacy_data["meta"]["category_stats"]["选择题"]}')
    print(f'分析题: {legacy_data["meta"]["category_stats"]["分析题"]}')
    print(f'简答题: {legacy_data["meta"]["category_stats"]["简答题"]}')
    print(f'已保存到: {output_path}')
    
    return legacy_data

if __name__ == '__main__':
    main()
