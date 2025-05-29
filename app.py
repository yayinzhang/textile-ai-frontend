from flask import Flask, request, jsonify
from flask_cors import CORS
import requests
from flask import render_template

app = Flask(__name__)
CORS(app)  # 允許前端跨域請求

@app.route('/')
def home():
    return render_template('chat.html')

# 替換成你自己的 Dify API 金鑰
DIFY_API_KEY = 'app-eBJH00k56FXJoIYyvTiERAHg'
DIFY_API_URL = 'http://dify.ecofabrics.world/v1/chat-messages'

@app.route('/chat', methods=['POST'])
def chat():
    data = request.get_json()
    user_query = data.get('query', '')
    user_id = data.get('user', 'test')  # 從前端取得 user，如果沒有則為 test

    print("❓ 使用者輸入：", user_query)
    print("🔒 使用者 ID:", user_id)

    # 發送請求到 Dify API
    response = requests.post(
        DIFY_API_URL,
        headers={
            'Authorization': f'Bearer {DIFY_API_KEY}',
            'Content-Type': 'application/json'
        },
        json={
            # 前端僅傳來 query 與 user，後端補上 inputs
            'inputs': {},
            'query': user_query,
            'user': user_id
        }
    )

    if response.status_code == 200:
        res_json = response.json()
        # 假設 Dify 回傳的回答在 'answer' 欄位
        answer = res_json.get('answer', None)
        if not answer:
            # 如果找不到 answer 欄位，嘗試用其他欄位或回傳整體
            answer = res_json.get('output', '❌ 無法取得回答，請稍後再試。')
        return jsonify({'answer': answer})
    else:
        return jsonify({'answer': '❌ 後端錯誤，請稍後再試。'}), 500

if __name__ == '__main__':
    app.run(debug=True)