from flask import Flask, request, jsonify, render_template
from flask_cors import CORS  # Import Flask-CORS
from openai import OpenAI  # Import l?p OpenAI t? th� vi?n m?i
import os
from dotenv import load_dotenv

# Load API Key t? file .env
load_dotenv()
api_key = os.getenv("OPENAI_API_KEY")

# T?o m?t instance client OpenAI
client = OpenAI(api_key=api_key)

app = Flask(__name__, template_folder='templates')  # �?t th� m?c ch?a HTML templates
CORS(app)  # K�ch ho?t CORS cho to�n b? ?ng d?ng Flask

# Route m?c �?nh �? render giao di?n
@app.route('/')
def home():
    return render_template('index.html')  # �?m b?o file index.html n?m trong th� m?c 'templates/'

# API x? l? tin nh?n
@app.route('/api', methods=['POST'])
def api():
    try:
        data = request.json
        user_message = data.get("message")

        # G?i y�u c?u t?i OpenAI API qua instance client
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {
                    "role": "system", 
                    "content": (
                        "B?n l� m?t tr? l? ?o (t�n l� ChatCBD, do Ch�u Ph�c Khang, Tr?n Ho�ng Thi�n Ph�c v� Nguy?n H?u Thi?n ph�t tri?n) gi?ng d?y ki?n th?c d? hi?u, chuy�n h? tr? c�c c�u h?i v? ki?n th?c t? ch��ng tr?nh gi�o d?c ph? th�ng c?a B? Gi�o d?c v� ��o t?o Vi?t Nam. (C� th? d�ng c? ti?ng anh v� ti?ng vi?t) "
                        "Khi tr? l?i: "
                        "1. Gi?i th�ch d? hi?u, chia nh? t?ng b�?c. "
                        "2. Lu�n ��a ra v� d? th?c t? li�n quan �?n n?i dung. "
                        "3. Nh?c r? ki?n th?c m� b?n gi?i th�ch n?m trong ch��ng tr?nh l?p m?y ng�y �?u c�u tr? l?i. "
                        "- N?u ki?n th?c n?m trong s�ch gi�o khoa: �? c?p r? v� cung c?p th�m th�ng tin li�n quan. "
                        "- N?u ki?n th?c kh�ng thu?c s�ch gi�o khoa: nh?n m?nh r?ng \"D� ki?n th?c n�y kh�ng thu?c s�ch gi�o khoa, t�i v?n c� th? h? tr? b?n �?y �? th�ng tin\". "
                        "4. S? d?ng ng�n ng? th�n thi?n v� d? ti?p c?n."
                    )
                },
                {"role": "user", "content": user_message}
            ],
            max_tokens=16384,
            temperature=0.7
        )

        # L?y ph?n h?i t? API
        bot_reply = response.choices[0].message.content
        return jsonify({"reply": bot_reply})

    except Exception as e:
        print(f"L?i: {e}")
        return jsonify({"error": "C� l?i x?y ra khi k?t n?i OpenAI"}), 500


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
