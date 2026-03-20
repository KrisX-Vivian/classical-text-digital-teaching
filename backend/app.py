import os
import json
from pathlib import Path
from flask import Flask, request, jsonify, Response, stream_with_context
from flask_cors import CORS
from openai import OpenAI
from dotenv import load_dotenv

# 获取当前文件（app.py）所在的目录，即 backend 目录
basedir = Path(__file__).parent
# 加载 backend 目录下的 .env 文件
load_dotenv(basedir / '.env')

app = Flask(__name__)
# 允许前端跨域请求（非常重要！）
CORS(app)

# 初始化 OpenAI 客户端，指向阿里云百炼的端点
# 阿里云百炼的 API 兼容 OpenAI 的接口格式，这让我们能用熟悉的库来调用[citation:5][citation:8]
client = OpenAI(
    api_key=os.getenv("DASHSCOPE_API_KEY"),
    base_url="https://dashscope.aliyuncs.com/compatible-mode/v1"  # 这是通用的兼容接口地址[citation:8]
)

@app.route('/api/chat', methods=['POST'])
def chat():
    try:
        data = request.get_json()
        user_message = data.get('message', '')

        if not user_message:
            return jsonify({'error': '消息不能为空'}), 400

        # 构建消息历史，这里可以加入 system prompt 来定义 AI 的角色
        messages = [
            {"role": "system", "content": "你是一位专业的古典文学助手，擅长解答《红楼梦》等古典名著的相关问题。"},
            {"role": "user", "content": user_message}
        ]

        # 调用通义千问模型
        # 关于模型的选择，可以参考阿里云的定价文档[citation:4]，qwen-plus 是性价比很高的选择
        completion = client.chat.completions.create(
            model="qwen-plus",  # 也可以换成 qwen-turbo (更快) 或 qwen-max (更强)
            messages=messages,
            temperature=0.7,  # 控制创造性的参数
            stream=True       # 开启流式输出，让用户体验更好
        )

        # 使用流式响应，将内容逐段返回给前端
        def generate():
            for chunk in completion:
                # 从响应流中提取内容
                if chunk.choices[0].delta.content is not None:
                    yield chunk.choices[0].delta.content

        return Response(stream_with_context(generate()), mimetype='text/plain')

    except Exception as e:
        print(f"调用API出错: {e}")
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    # 运行在 5000 端口，开启调试模式
    app.run(host='0.0.0.0', port=5000, debug=True)