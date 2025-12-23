from flask import Flask, render_template, request, jsonify, session
from huggingface_hub import InferenceClient
import os
from config import Config
from info import PHOTO_GALLERY, BOT_CONFIG

app = Flask(__name__)
app.secret_key = "RAJ_DEV_SECURE_2025"

# Hugging Face Client Setup
client = InferenceClient(api_key=os.environ.get("HF_TOKEN") or Config.HF_TOKEN)

@app.route('/')
def index():
    # Nayi session history shuru karein
    session['history'] = [] 
    
    # HTML ko saara zaroori data bhejna (Social Links, Photos, etc.)
    return render_template('index.html', 
                           name=BOT_CONFIG["NAME"], 
                           avatar_n=BOT_CONFIG["AVATAR_NORMAL"],
                           photos=PHOTO_GALLERY,
                           smart_link=BOT_CONFIG["SMARTLINK_URL"],
                           config_links=BOT_CONFIG) # Social buttons fix ke liye

@app.route('/chat', methods=['POST'])
def chat():
    try:
        user_message = request.json.get("message")
        
        # Chat history manage karna (Memory)
        if 'history' not in session: 
            session['history'] = []
        
        history = session['history']
        history.append({"role": "user", "content": user_message})
        
        # Limit history to last 15 messages for speed
        if len(history) > 15: 
            history = history[-15:]

        # AI Response generate karna
        messages = [{"role": "system", "content": Config.SYSTEM_INSTRUCTION}] + history
        
        completion = client.chat_completion(
            model=Config.MODEL_ID, 
            messages=messages, 
            max_tokens=150
        )
        
        reply = completion.choices[0].message.content
        
        # Assistant ka reply history mein jodhna
        history.append({"role": "assistant", "content": reply})
        session['history'] = history
        
        return jsonify({"reply": reply})
        
    except Exception as e:
        print(f"Error occurred: {e}")
        return jsonify({"reply": "Maaf kijiye, abhi mera system thoda busy hai. Kuch der baad koshish karein."})

if __name__ == '__main__':
    # Koyeb ke liye port setup
    port = int(os.environ.get("PORT", 8000))
    app.run(host='0.0.0.0', port=port)
    
