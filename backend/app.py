from flask import Flask, request, jsonify
import openai
import os

app = Flask(__name__)

# Đặt OpenAI API key
openai.api_key = os.getenv("OPENAI_API_KEY")

@app.route('/chat', methods=['POST'])
def chat():
    user_input = request.json.get('message')
    response = openai.ChatCompletion.create(
        model="gpt-4o",
        messages=[{"role": "user", "content": user_input}]
    )
    return jsonify({'response': response['choices'][0]['message']['content']})

if __name__ == '__main__':
    app.run(debug=True)