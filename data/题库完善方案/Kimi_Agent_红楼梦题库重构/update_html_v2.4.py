import json
import os
import re

def update_exercises_html():
    json_path = r'd:\大创项目\classical-literature-ai-web\data\红楼梦题库--txt版本\hongloumeng_questions_v2.4_legacy.json'
    html_path = r'd:\大创项目\classical-literature-ai-web\exercises.html'
    
    with open(json_path, 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    questions = data['questions']
    
    questions_json = json.dumps(questions, ensure_ascii=False)
    
    html_template = '''<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>古典文本数字化教学平台 - 题库与AI</title>
    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.min.css" rel="stylesheet">
    <link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/bootstrap-icons@1.10.5/font/bootstrap-icons.css">
    <link href="https://fonts.googleapis.com/css2?family=Noto+Serif+SC:wght@400;600;700&display=swap" rel="stylesheet">
    <link rel="stylesheet" href="assets/css/style.css?v=4">
    <link rel="stylesheet" href="assets/css/navbar-advanced.css?v=2">
    <link rel="stylesheet" href="assets/css/exercises-optimized.css">
    <link rel="stylesheet" href="assets/css/scroll-unfolding.css?v=1">
    <style>
        .filter-nav-section {
            background: linear-gradient(135deg, #f9f5ed 0%, #f0e6d2 100%);
            border: 2px solid #8b5a2b;
            border-radius: 8px;
            padding: 20px;
            box-shadow: 0 4px 15px rgba(139, 90, 43, 0.2);
        }
        
        .filter-btn-group {
            display: flex;
            flex-wrap: wrap;
            gap: 10px;
            justify-content: center;
        }
        
        .filter-btn {
            padding: 12px 24px;
            border: 2px solid #8b5a2b;
            background: #f9f5ed;
            color: #5d3a1a;
            font-family: "Noto Serif SC", "楷体", serif;
            font-size: 15px;
            cursor: pointer;
            border-radius: 6px;
            transition: all 0.3s ease;
            display: flex;
            align-items: center;
            gap: 8px;
        }
        
        .filter-btn:hover {
            background: #e8d9bc;
            transform: translateY(-2px);
            box-shadow: 0 4px 12px rgba(139, 90, 43, 0.3);
        }
        
        .filter-btn.active {
            background: #8b5a2b;
            color: #f9f5ed;
            border-color: #a06c3b;
        }
        
        .filter-btn i {
            font-size: 18px;
        }
        
        .questions-container {
            display: none;
            margin-top: 20px;
        }
        
        .questions-container.show {
            display: block;
        }
        
        .question-group {
            margin-bottom: 15px;
            border: 1px dashed #a06c3b;
            border-radius: 8px;
            background: #fdfbf7;
            overflow: visible;
        }
        
        .question-header {
            padding: 15px 20px;
            background: linear-gradient(135deg, #f0e6d2 0%, #e8d9bc 100%);
            cursor: pointer;
            display: flex;
            justify-content: space-between;
            align-items: center;
            transition: all 0.3s ease;
        }
        
        .question-header:hover {
            background: linear-gradient(135deg, #e8d9bc 0%, #dcc9a8 100%);
        }
        
        .question-header h3 {
            margin: 0;
            font-size: 16px;
            color: #5d3a1a;
            font-family: "Noto Serif SC", "楷体", serif;
            flex: 1;
            line-height: 1.6;
            overflow: visible;
            word-wrap: break-word;
        }
        
        .question-meta {
            display: flex;
            align-items: center;
            gap: 10px;
            flex-shrink: 0;
            margin-left: 15px;
        }
        
        .fold-icon {
            color: #8b5a2b;
            font-size: 14px;
            transition: transform 0.3s ease;
        }
        
        .fold-icon.expanded {
            transform: rotate(180deg);
        }
        
        .type-tag {
            background: #e8d9bc;
            color: #8b5a2b;
            padding: 4px 12px;
            border-radius: 20px;
            font-size: 12px;
            font-family: "Noto Serif SC", "楷体", serif;
            white-space: nowrap;
        }
        
        .question-body {
            display: none;
            padding: 20px;
            background: #fdfbf7;
            border-top: 1px solid #e8d9bc;
        }
        
        .question-body.show {
            display: block;
            animation: slideDown 0.3s ease;
        }
        
        @keyframes slideDown {
            from { opacity: 0; transform: translateY(-10px); }
            to { opacity: 1; transform: translateY(0); }
        }
        
        .exercise-options .form-check {
            padding: 10px 15px;
            margin: 8px 0;
            border: 1px solid #e0d5c5;
            border-radius: 6px;
            background: #fff;
            transition: all 0.2s ease;
        }
        
        .exercise-options .form-check:hover {
            border-color: #8b5a2b;
            background: #faf6ef;
        }
        
        .exercise-options .form-check-input:checked + .form-check-label {
            color: #8b5a2b;
            font-weight: 600;
        }
        
        .answer-card {
            background: #fdfbf7;
            border-left: 4px solid #8b5a2b;
            padding: 15px;
            margin-top: 15px;
            border-radius: 4px;
        }
        
        .correct-answer {
            color: #8b5a2b;
            font-size: 16px;
        }
        
        .textarea-form-control {
            width: 100%;
            padding: 12px 15px;
            border: 2px solid #dcc9a8;
            border-radius: 6px;
            background: #fdfbf7;
            font-family: "Noto Serif SC", "楷体", serif;
            font-size: 14px;
            resize: vertical;
            min-height: 100px;
            transition: border-color 0.3s ease;
        }
        
        .textarea-form-control:focus {
            outline: none;
            border-color: #8b5a2b;
            box-shadow: 0 0 0 3px rgba(139, 90, 43, 0.1);
        }
        
        .guofeng-btn {
            background: linear-gradient(135deg, #8b5a2b 0%, #a06c3b 100%);
            color: #f9f5ed;
            border: none;
            padding: 10px 20px;
            border-radius: 6px;
            font-family: "Noto Serif SC", "楷体", serif;
            cursor: pointer;
            transition: all 0.3s ease;
            display: inline-flex;
            align-items: center;
            gap: 8px;
        }
        
        .guofeng-btn:hover {
            transform: translateY(-2px);
            box-shadow: 0 4px 15px rgba(139, 90, 43, 0.4);
        }
        
        .keyword {
            color: #8b5a2b;
            font-weight: 600;
        }
        
        .empty-tip {
            text-align: center;
            padding: 40px;
            color: #a08060;
            font-family: "Noto Serif SC", "楷体", serif;
            font-size: 16px;
        }
        
        .empty-tip i {
            font-size: 48px;
            margin-bottom: 15px;
            display: block;
        }
    </style>
</head>
<body>
    <nav class="navbar navbar-expand-lg navbar-dark fixed-top">
        <div class="container">
            <a class="navbar-brand" href="index.html">典籍新诠</a>
            <button class="navbar-toggler" type="button" data-bs-toggle="collapse" data-bs-target="#navbarNav">
                <span class="navbar-toggler-icon"></span>
            </button>
            <div class="collapse navbar-collapse" id="navbarNav">
                <ul class="navbar-nav ms-auto">
                    <li class="nav-item"><a class="nav-link" href="index.html">首页</a></li>
                    <li class="nav-item"><a class="nav-link" href="resource.html">资源库</a></li>
                    <li class="nav-item"><a class="nav-link" href="courses.html">教学视频</a></li>
                    <li class="nav-item"><a class="nav-link active" href="exercises.html">题库与AI</a></li>
                </ul>
            </div>
        </div>
    </nav>

    <div class="page-bg-video">
        <video class="page-bg-video-media" autoplay muted loop playsinline preload="metadata">
            <source src="assets/videos/LandscapePainting.mp4" type="video/mp4">
        </video>
    </div>

    <div class="page-header">
        <div class="container">
            <h1>互动题库与智能助手</h1>
            <p>通过多样化的习题巩固知识，更有专属AI助手为你答疑解惑</p>
        </div>
    </div>

    <div class="container">
        <div class="row g-4">
            <div class="col-lg-6 exercise-module">
                <h2 class="h4 mb-4">精选题库</h2>
                
                <!-- 互动小游戏按钮 -->
                <div class="mb-4">
                    <button class="filter-btn" onclick="openGame()" style="background: linear-gradient(135deg, #a06c3b 0%, #8b5a2b 100%); color: #f9f5ed; border-color: #a06c3b;">
                        <i class="bi bi-controller"></i> 开始小游戏
                    </button>
                </div>
                
                <div class="filter-nav-section mb-4">
                    <div class="filter-btn-group">
                        <button class="filter-btn active" data-filter="all" onclick="showQuestions('all')">
                            <i class="bi bi-grid-3x3-gap"></i>全部题目
                        </button>
                        <button class="filter-btn" data-filter="choice" onclick="showQuestions('choice')">
                            <i class="bi bi-list-check"></i>选择题
                        </button>
                        <button class="filter-btn" data-filter="short" onclick="showQuestions('short')">
                            <i class="bi bi-pencil-square"></i>简答题
                        </button>
                        <button class="filter-btn" data-filter="analysis" onclick="showQuestions('analysis')">
                            <i class="bi bi-journal-text"></i>分析题
                        </button>
                        <button class="filter-btn" data-filter="collapse" onclick="collapseAll()">
                            <i class="bi bi-chevron-double-up"></i>收起全部
                        </button>
                    </div>
                </div>

                <div class="questions-container" id="questionsContainer"></div>

                <div class="empty-tip" id="emptyTip">
                    <i class="bi bi-journal-bookmark"></i>
                    <p>请点击上方按钮选择题型查看题目</p>
                </div>
            </div>

            <div class="col-lg-1 d-none d-lg-block">
                <div class="section-divider"></div>
            </div>

            <div class="col-lg-5 ai-tool-module">
                <div class="ai-tool-card">
                    <div class="digital-pattern"></div>
                    <i class="bi bi-robot tool-icon"></i>
                    <h3>专属AI助手</h3>
                    <p>输入您关于《红楼梦》或古籍的问题，AI将为您提供专业解答。</p>
                    
                    <div class="d-flex">
                        <input type="text" class="ai-input" id="userInput" placeholder="请输入需解析的古典文本内容...">
                        <button class="ai-btn" onclick="sendToDoubao()">
                            <i class="bi bi-send"></i>
                        </button>
                    </div>
                    
                    <div class="ai-response-box mt-4" id="aiResponse">
                        <span class="ai-label"><i class="bi bi-robot"></i> AI助手回答：</span>
                        <p class="text-muted">AI回答将显示在这里...</p>
                    </div>
                </div>
            </div>
        </div>
    </div>

    <button class="back-to-top" id="backToTop" title="回到顶部">
        <i class="bi bi-arrow-up"></i>
    </button>

    <footer>
        <div class="container">
            <div class="text-center">
                <p>© 2026 典籍新诠 - 古典文本数字化教学平台 版权所有</p>
                <p class="text-muted small mt-2">本平台仅用于教学研究使用</p>
            </div>
        </div>
    </footer>

    <script src="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/js/bootstrap.bundle.min.js"></script>
    <script>
        window.addEventListener('scroll', function() {
            const navbar = document.querySelector('.navbar');
            if (window.scrollY > 50) {
                navbar.classList.add('scrolled');
            } else {
                navbar.classList.remove('scrolled');
            }
        });
        
        const BACKEND_API_URL = '/api/ai/chat';
        
        const questionsData = QUESTIONS_PLACEHOLDER;

        let currentFilter = '';
        
        function showQuestions(filter) {
            const container = document.getElementById('questionsContainer');
            const emptyTip = document.getElementById('emptyTip');
            
            document.querySelectorAll('.filter-btn').forEach(btn => {
                btn.classList.remove('active');
            });
            document.querySelector('[data-filter="' + filter + '"]').classList.add('active');
            
            currentFilter = filter;
            emptyTip.style.display = 'none';
            container.classList.add('show');
            
            let filteredQuestions = [];
            if (filter === 'all') {
                filteredQuestions = questionsData;
            } else if (filter === 'choice') {
                filteredQuestions = questionsData.filter(q => q.type === '选择题');
            } else if (filter === 'short') {
                filteredQuestions = questionsData.filter(q => q.type === '简答题');
            } else if (filter === 'analysis') {
                filteredQuestions = questionsData.filter(q => q.type === '分析题');
            }
            
            container.innerHTML = generateQuestionsHTML(filteredQuestions);
        }
        
        function collapseAll() {
            const container = document.getElementById('questionsContainer');
            const emptyTip = document.getElementById('emptyTip');
            
            document.querySelectorAll('.filter-btn').forEach(btn => {
                btn.classList.remove('active');
            });
            
            container.classList.remove('show');
            container.innerHTML = '';
            emptyTip.style.display = 'block';
            currentFilter = '';
        }
        
        function generateQuestionsHTML(questions) {
            if (questions.length === 0) {
                return '<div class="empty-tip"><i class="bi bi-inbox"></i><p>暂无题目</p></div>';
            }
            
            let html = '';
            questions.forEach((q, index) => {
                const typeIcon = q.type === '选择题' ? 'bi-list-check' : (q.type === '简答题' ? 'bi-pencil-square' : 'bi-journal-text');
                const displayQuestion = q.question.replace(/《红楼梦》/g, '<span class="keyword">《红楼梦》</span>');
                const cleanNum = parseInt(q.id.replace('hrm-', ''), 10);
                const displayNum = '第' + cleanNum + '题';
                
                html += '<div class="question-group" data-id="' + q.id + '">';
                html += '  <div class="question-header" onclick="toggleQuestion(\\'' + q.id + '\\')">';
                html += '    <h3>' + displayNum + '. ' + displayQuestion + '</h3>';
                html += '    <div class="question-meta">';
                html += '      <span class="type-tag"><i class="bi ' + typeIcon + '"></i> ' + q.type + '</span>';
                html += '      <i class="bi bi-chevron-down fold-icon" id="icon-' + q.id + '"></i>';
                html += '    </div>';
                html += '  </div>';
                html += '  <div class="question-body" id="body-' + q.id + '">';
                
                if (q.type === '选择题' && q.options) {
                    html += '    <p class="exercise-content">请从以下选项中选择正确答案：</p>';
                    html += '    <div class="exercise-options mb-3">';
                    q.options.forEach((opt, i) => {
                        html += '      <div class="form-check">';
                        html += '        <input class="form-check-input" type="radio" name="' + q.id + '" id="' + q.id + '-opt' + i + '">';
                        html += '        <label class="form-check-label" for="' + q.id + '-opt' + i + '">' + opt + '</label>';
                        html += '      </div>';
                    });
                    html += '    </div>';
                } else {
                    html += '    <p class="exercise-content">请简述你的理解：</p>';
                    html += '    <textarea class="textarea-form-control mb-3" rows="4" placeholder="请输入你的答案..."></textarea>';
                }
                
                html += '    <button class="guofeng-btn" type="button" data-bs-toggle="collapse" data-bs-target="#' + q.id + '-answer">';
                html += '      <i class="bi bi-eye"></i> 查看答案/解析';
                html += '    </button>';
                html += '    <div class="collapse mt-3" id="' + q.id + '-answer">';
                html += '      <div class="answer-card">';
                if (q.answer) {
                    html += '        <p><strong class="correct-answer">答案：</strong>' + q.answer + '</p>';
                }
                html += '        <p><strong>解析：</strong>请参考《红楼梦》原著相关内容进行解析。</p>';
                html += '      </div>';
                html += '    </div>';
                html += '  </div>';
                html += '</div>';
            });
            
            return html;
        }
        
        function toggleQuestion(id) {
            const body = document.getElementById('body-' + id);
            const icon = document.getElementById('icon-' + id);
            
            if (body.classList.contains('show')) {
                body.classList.remove('show');
                icon.classList.remove('expanded');
            } else {
                body.classList.add('show');
                icon.classList.add('expanded');
            }
        }
        
        const GAME_LINK = 'https://api.ourteacher.cc/api/html/detail?md5=d2bc5bf73918f968f1bc66cd95fcc7b0&user_id=10029784';
        
        function openGame() {
            window.open(GAME_LINK, '_blank');
        }
        
        async function sendToDoubao() {
            const userInput = document.getElementById('userInput').value.trim();
            const aiResponse = document.getElementById('aiResponse');
            
            if (!userInput) {
                aiResponse.innerHTML = '<span class="ai-label"><i class="bi bi-robot"></i> AI助手回答：</span><p style="color: #DC143C;">请输入您的问题！</p>';
                return;
            }
            
            aiResponse.innerHTML = '<span class="ai-label"><i class="bi bi-robot"></i> AI助手回答：</span><div class="loading-spinner"></div>';
            
            try {
                const response = await fetch(BACKEND_API_URL, {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify({ question: userInput })
                });
                
                if (!response.ok) throw new Error('HTTP错误: ' + response.status);
                
                const data = await response.json();
                const answer = data.answer || data.choices?.[0]?.message?.content;
                
                if (answer) {
                    aiResponse.innerHTML = '<span class="ai-label"><i class="bi bi-robot"></i> AI助手回答：</span><div style="line-height: 1.8;">' + answer.replace(/\\n/g, '<br>') + '</div>';
                } else {
                    throw new Error('返回数据格式不正确');
                }
            } catch (error) {
                console.error('调用AI服务出错:', error);
                aiResponse.innerHTML = '<span class="ai-label"><i class="bi bi-robot"></i> AI助手回答：</span><p style="color: #DC143C;"><i class="bi bi-exclamation-triangle"></i> 调用失败：' + error.message + '</p><p class="text-muted small mt-2">当前后端API地址：' + BACKEND_API_URL + '</p>';
            }
        }
        
        document.getElementById('userInput').addEventListener('keypress', function(e) {
            if (e.key === 'Enter') sendToDoubao();
        });

        const backToTopBtn = document.getElementById('backToTop');
        window.addEventListener('scroll', function() {
            if (window.scrollY > 300) {
                backToTopBtn.classList.add('show');
            } else {
                backToTopBtn.classList.remove('show');
            }
        });
        backToTopBtn.addEventListener('click', function() {
            window.scrollTo({ top: 0, behavior: 'smooth' });
        });
    </script>
    <script src="assets/js/scroll-unfolding.js"></script>
</body>
</html>'''
    
    final_html = html_template.replace('QUESTIONS_PLACEHOLDER', questions_json)
    
    with open(html_path, 'w', encoding='utf-8') as f:
        f.write(final_html)
    
    print(f'成功更新exercises.html，共{len(questions)}道题目')

if __name__ == '__main__':
    update_exercises_html()
