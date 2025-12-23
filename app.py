from flask import Flask, render_template, request, jsonify, session
from huggingface_hub import InferenceClient
import os
from config import Config
from info import PHOTO_GALLERY, BOT_CONFIG

app = Flask(__name__)
app.secret_key = "DEV_RAJ_2025"

client = InferenceClient(api_key=os.environ.get("HF_TOKEN") or Config.HF_TOKEN)

@app.route('/')
def index():
    session['history'] = [] 
    return render_template('index.html', 
                           name=BOT_CONFIG["NAME"], 
                           avatar_n=BOT_CONFIG["AVATAR_NORMAL"],
                           avatar_t=BOT_CONFIG["AVATAR_TALKING"],
                           photos=PHOTO_GALLERY,
                           smart_link=BOT_CONFIG["SMARTLINK_URL"])

@app.route('/chat', methods=['POST'])
def chat():
    try:
        user_message = request.json.get("message")
        if 'history' not in session: session['history'] = []
        history = session['history']
        history.append({"role": "user", "content": user_message})
        if len(history) > 20: history = history[-20:]

        messages = [{"role": "system", "content": Config.SYSTEM_INSTRUCTION}] + history
        completion = client.chat_completion(model=Config.MODEL_ID, messages=messages, max_tokens=200)
        reply = completion.choices[0].message.content
        
        history.append({"role": "assistant", "content": reply})
        session['history'] = history
        return jsonify({"reply": reply})
    except:
        return jsonify({"reply": "System busy hai."})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=int(os.environ.get("PORT", 8000)))
    
