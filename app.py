from flask import Flask, render_template, request, jsonify, session
from huggingface_hub import InferenceClient
import os
from config import Config
from info import PHOTO_GALLERY, BOT_CONFIG

app = Flask(__name__)
app.secret_key = "RAJS_SECRET_KEY" # Memory ke liye zaroori hai

hf_token = os.environ.get("HF_TOKEN") or Config.HF_TOKEN
client = InferenceClient(api_key=hf_token)
MODEL_ID = Config.MODEL_ID

@app.route('/')
def index():
    # Jab page refresh ho, to purani memory saaf karne ke liye (optional)
    session['history'] = [] 
    return render_template('index.html', 
                           name=BOT_CONFIG["NAME"], 
                           avatar=BOT_CONFIG["AVATAR"],
                           photos=PHOTO_GALLERY,
                           smart_link=BOT_CONFIG["SMARTLINK_URL"])

@app.route('/chat', methods=['POST'])
def chat():
    try:
        data = request.get_json()
        user_message = data.get("message")

        # Session se purani history nikalna
        if 'history' not in session:
            session['history'] = []
        
        history = session['history']

        # Naya message history mein jodna
        history.append({"role": "user", "content": user_message})

        # Memory Limit: Sirf last 20 messages rakhna
        if len(history) > 20:
            history = history[-20:]

        # AI ko bhejne ke liye messages taiyar karna
        messages = [{"role": "system", "content": Config.SYSTEM_INSTRUCTION}] + history

        completion = client.chat_completion(
            model=MODEL_ID,
            messages=messages,
            max_tokens=500
        )
        
        reply = completion.choices[0].message.content
        
        # AI ka jawab bhi history mein save karna
        history.append({"role": "assistant", "content": reply})
        session['history'] = history # Session update karna
        
        return jsonify({"reply": reply})
        
    except Exception as e:
        return jsonify({"reply": "System busy hai, thodi der mein try karein."})

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 8000))
    app.run(host='0.0.0.0', port=port)
    
