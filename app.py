from flask import Flask, render_template, request, jsonify, session
from huggingface_hub import InferenceClient
import os
from config import Config
from info import PHOTO_GALLERY, BOT_CONFIG

app = Flask(__name__)
app.secret_key = "RAJ_DEV_SECURE_2025"

# Global timeout for the client
client = InferenceClient(
    api_key=os.environ.get("HF_TOKEN") or Config.HF_TOKEN,
    timeout=120
)

@app.route('/')
def index():
    session['history'] = [] 
    return render_template('index.html', 
                           name=BOT_CONFIG["NAME"], 
                           avatar_n=BOT_CONFIG["AVATAR_NORMAL"],
                           photos=PHOTO_GALLERY,
                           smart_link=BOT_CONFIG["SMARTLINK_URL"],
                           config_links=BOT_CONFIG)

@app.route('/chat', methods=['POST'])
def chat():
    try:
        user_message = request.json.get("message")
        if 'history' not in session: session['history'] = []
        history = session['history']
        history.append({"role": "user", "content": user_message})
        if len(history) > 10: history = history[-10:]

        messages = [{"role": "system", "content": Config.SYSTEM_INSTRUCTION}] + history
        
        completion = client.chat_completion(
            model=Config.MODEL_ID, 
            messages=messages, 
            max_tokens=120
        )
        
        reply = completion.choices[0].message.content
        history.append({"role": "assistant", "content": reply})
        session['history'] = history
        return jsonify({"reply": reply})
        
    except Exception as e:
        return jsonify({"reply": "System busy hai, please refresh karein."})

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 8000))
    app.run(host='0.0.0.0', port=port)
    
