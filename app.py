from flask import Flask, render_template, request, jsonify, session
from huggingface_hub import InferenceClient
import os
from config import Config
from info import PHOTO_GALLERY, BOT_CONFIG

app = Flask(__name__)
app.secret_key = "RAJ_DEV_SECURE_2025"

# Client Setup
client = InferenceClient(
    api_key=os.environ.get("HF_TOKEN") or Config.HF_TOKEN,
    timeout=120
)

@app.route('/')
def index():
    session.clear()
    return render_template('index.html', 
                           name=BOT_CONFIG["NAME"], 
                           avatar_n=BOT_CONFIG["AVATAR_NORMAL"],
                           photos=PHOTO_GALLERY,
                           smart_link=BOT_CONFIG["SMARTLINK_URL"],
                           config_links=BOT_CONFIG)

@app.route('/chat', methods=['POST'])
def chat():
    try:
        data = request.json
        user_message = data.get("message", "").lower() # Message ko chhota (lowercase) kar diya
        
        if not user_message: return jsonify({"reply": "Kuch boliye..."})

        # --- 1. DIRECT OVERRIDE (AI KO BYPASS KARO) ---
        # Agar koi ye puche, to seedha hardcoded jawab do. AI se mat puncho.
        triggers = ["kisne banaya", "who made you", "creator", "owner", "malik", "kaun hai tera creator", "who created you", "meta", "facebook"]
        
        if any(word in user_message for word in triggers):
            return jsonify({"reply": "Mujhe Raj Dev ne banaya hai. Main unka personal AI assistant hoon."})

        # --- 2. AGAR NORMAL BAAT HAI TO AI SE PUNCHO ---
        if 'history' not in session: session['history'] = []
        history = session['history']
        
        history.append({"role": "user", "content": user_message})
        if len(history) > 4: history = history[-4:]

        # System Prompt (Backup ke liye)
        system_instruction = {
            "role": "system", 
            "content": "You are Dev, an AI assistant created by Raj Dev. Answer briefly in Hinglish."
        }
        
        messages = [system_instruction] + history
        
        completion = client.chat_completion(
            model=Config.MODEL_ID, 
            messages=messages, 
            max_tokens=150,
            temperature=0.5
        )
        
        reply = completion.choices[0].message.content
        
        # Double Check: Agar AI ne galti se Meta bol diya, to replace kar do
        if "Meta" in reply or "Facebook" in reply:
            reply = "Mujhe Raj Dev ne develop kiya hai."

        history.append({"role": "assistant", "content": reply})
        session['history'] = history
        
        return jsonify({"reply": reply})
        
    except Exception as e:
        print(f"Error: {e}")
        return jsonify({"reply": "Network issue. Dobara puchiye."})

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 8000))
    app.run(host='0.0.0.0', port=port)
    
