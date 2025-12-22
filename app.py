# --- app.py ---
from flask import Flask, render_template, request, jsonify
import google.generativeai as genai
import os
from config import Config
from info import PHOTO_GALLERY, BOT_CONFIG

app = Flask(__name__)

api_key = os.environ.get("GEMINI_API_KEY") or Config.API_KEY
genai.configure(api_key=api_key)

# 2025 Latest Gemini 2.5 Flash Model
model = genai.GenerativeModel(
    model_name="gemini-2.5-flash", 
    system_instruction=Config.SYSTEM_INSTRUCTION
)

@app.route('/')
def index():
    return render_template('index.html', 
                           name=BOT_CONFIG["NAME"], 
                           avatar=BOT_CONFIG["AVATAR"],
                           news_link=BOT_CONFIG["NEWS_LINK"],
                           telegram_link=BOT_CONFIG["TELEGRAM_LINK"],
                           whatsapp_link=BOT_CONFIG["WHATSAPP_LINK"],
                           facebook_link=BOT_CONFIG["FACEBOOK_LINK"],
                           instagram_link=BOT_CONFIG["INSTAGRAM_LINK"],
                           photos=PHOTO_GALLERY)

@app.route('/chat', methods=['POST'])
def chat():
    try:
        data = request.get_json()
        user_message = data.get("message")
        chat_session = model.start_chat(history=[])
        response = chat_session.send_message(user_message)
        return jsonify({"reply": response.text})
    except Exception as e:
        return jsonify({"reply": "System Error: " + str(e)})

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 8000))
    app.run(host='0.0.0.0', port=port)
    
