from flask import Flask, render_template, request, jsonify
import google.generativeai as genai
import os
from config import Config
from info import PHOTO_GALLERY, BOT_CONFIG

app = Flask(__name__)

# API Key check karne ke liye logic
api_key = os.environ.get("GEMINI_API_KEY")
if not api_key:
    # Agar Koyeb se key nahi mili, toh config.py se le
    api_key = Config.API_KEY

genai.configure(api_key=api_key)

# Gemini 2.0 Flash use kar rahe hain
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
                           photos=PHOTO_GALLERY)

@app.route('/chat', methods=['POST'])
def chat():
    try:
        data = request.get_json()
        user_message = data.get("message")
        
        if not user_message:
            return jsonify({"reply": "Aapne kuch likha nahi!"})

        # Naya Chat session shuru karein
        chat_session = model.start_chat(history=[])
        response = chat_session.send_message(user_message)
        
        return jsonify({"reply": response.text})
    except Exception as e:
        print(f"ERROR: {str(e)}") # Ye error Koyeb logs mein dikhega
        return jsonify({"reply": "Maaf kijiye, abhi main connection nahi bana pa raha hoon."})

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 8000))
    app.run(host='0.0.0.0', port=port)
    
