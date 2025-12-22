from flask import Flask, render_template, request, jsonify
import google.generativeai as genai
import os
from config import Config
from info import PHOTO_GALLERY, BOT_CONFIG

app = Flask(__name__)

genai.configure(api_key=Config.API_KEY)
model = genai.GenerativeModel(
    model_name="gemini-1.5-flash",
    system_instruction=Config.SYSTEM_INSTRUCTION
)

@app.route('/')
def index():
    return render_template('index.html', 
                           name=BOT_CONFIG["NAME"], 
                           avatar=BOT_CONFIG["AVATAR"],
                           news_link=BOT_CONFIG["NEWS_LINK"],
                           photos=PHOTO_GALLERY) # Photos yahan se ja rahi hain

@app.route('/chat', methods=['POST'])
def chat():
    user_message = request.json.get("message")
    try:
        chat_session = model.start_chat(history=[])
        response = chat_session.send_message(user_message)
        return jsonify({"reply": response.text})
    except Exception as e:
        return jsonify({"reply": "System busy hai, kripya thodi der baad koshish karein."})

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 8000))
    app.run(host='0.0.0.0', port=port)
  
