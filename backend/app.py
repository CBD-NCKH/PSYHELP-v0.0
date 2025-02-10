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

# API xử lý tin nhắn
@app.route('/api', methods=['POST'])
def api():
    try:
        username = request.args.get('username')
        if not username:
            return jsonify({"error": "Unauthorized. Username is missing."}), 401

        sheet = connect_google_sheet("ChatHistory")
        print(f"Connected to Google Sheet for user: {username}")

        data = request.json
        user_message = data.get("message")

        memory = get_user_conversation(sheet, username, max_rows=4)
        print(f"Retrieved memory: {memory}")

        memory_context = "\n".join([f"{row[2]}: {row[3]}" for row in memory if len(row) >= 4])
        print(f"Memory context: {memory_context}")

        keywords = extract_keywords_multilingual(user_message)
        db_result = query_sqlite_with_keywords("DatasetTable", keywords)

        db_context = "\n".join([f"Row {i+1}: {row}" for i, row in enumerate(db_result)])
        context = (
            f"Dữ liệu từ cơ sở dữ liệu:\n{db_context}\n\n"
            f"Lịch sử hội thoại:\n{memory_context}\n\n"
            f"Câu hỏi của người dùng: {user_message}"
        )

        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {
                    "role": "system",
                    "content": (
                        "Bạn là một trợ lý ảo giúp tư vấn tâm lý cho người dùng"
                    )
                },
                {"role": "user", "content": context}
            ],
            max_tokens=9999999999999999999999999999999999,
            temperature=0.7
        )

        bot_reply = response.choices[0].message.content

        save_to_google_sheet(sheet, username, "user", user_message)
        save_to_google_sheet(sheet, username, "assistant", bot_reply)

        return jsonify({"reply": bot_reply})

    except openai.exceptions.OpenAIError as e:
        return jsonify({'error': f'OpenAI API error: {str(e)}'}), 500
    except Exception as e:
        return jsonify({'error': f'Server error: {str(e)}'}), 500

if __name__ == '__main__':
    app.run(debug=True)
