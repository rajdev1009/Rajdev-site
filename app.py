# --- app.py ---
from flask import Flask, render_template, request, jsonify
from huggingface_hub import InferenceClient
import os
from config import Config
from info import PHOTO_GALLERY, BOT_CONFIG

app = Flask(__name__)

# Token configuration
hf_token = os.environ.get("HF_TOKEN") or Config.HF_TOKEN
client = InferenceClient(api_key=hf_token)

# Model ID (Llama 3.2 3B fast aur accurate hai)
MODEL_ID = "meta-llama/Llama-3.2-3B-Instruct"

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
                           smart_link=BOT_CONFIG["SMARTLINK_URL"],
                           photos=PHOTO_GALLERY)

@app.route('/chat', methods=['POST'])
def chat():
    try:
        data = request.get_json()
        user_message = data.get("message")
        
        # System instructions aur user message ko format karna
        messages = [
            {"role": "system", "content": Config.SYSTEM_INSTRUCTION},
            {"role": "user", "content": user_message}
        ]

        # Hugging Face API call
        completion = client.chat_completion(
            model=MODEL_ID,
            messages=messages,
            max_tokens=500
        )
        
        reply = completion.choices[0].message.content
        return jsonify({"reply": reply})
        
    except Exception as e:
        print(f"Error: {e}")
        return jsonify({"reply": "Maaf kijiyega, main abhi thoda busy hoon. Phir se try karein."})

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 8000))
    app.run(host='0.0.0.0', port=port)
    
