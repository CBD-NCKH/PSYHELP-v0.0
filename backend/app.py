from flask import Flask, request, jsonify, send_from_directory
import openai
import os
import asyncio

app = Flask(__name__, static_folder="../frontend", static_url_path="", template_folder="../frontend")

# Đặt OpenAI API key
openai.api_key = os.getenv("OPENAI_API_KEY")

# Route để hiển thị giao diện (frontend)
@app.route('/')
def serve_index():
    return send_from_directory(app.template_folder, "index.html")

# API Chatbot với giao diện đồng bộ (sử dụng asyncio.run để đóng gói lời gọi bất đồng bộ)
@app.route('/chat', methods=['POST'])
def chat():
    user_input = request.json.get('message')
    if not user_input:
        return jsonify({'error': 'Message is required'}), 400

    try:
        # Chạy hàm bất đồng bộ theo cách đồng bộ
        response = asyncio.run(
            openai.ChatCompletion.acreate(
                model="gpt-4o",
                messages=[{"role": "user", "content": user_input}]
            )
        )
        return jsonify({'response': response['choices'][0]['message']['content']})
    except openai.exceptions.OpenAIError as e:
        return jsonify({'error': f'OpenAI API error: {str(e)}'}), 500
    except Exception as e:
        return jsonify({'error': f'Server error: {str(e)}'}), 500

if __name__ == '__main__':
    app.run(debug=True)
