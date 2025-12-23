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
    session.clear() # Har baar refresh karne par nayi shuruwat
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
        if not user_message: return jsonify({"reply": "Kuch boliye..."})

        if 'history' not in session: session['history'] = []
        history = session['history']
        
        # User message add karein
        history.append({"role": "user", "content": user_message})
        
        # --- STRICT MEMORY CONTROL ---
        # Sirf last 4 messages yaad rakhega taaki confuse na ho
        if len(history) > 4: 
            history = history[-4:]

        # --- STRICT INSTRUCTION ---
        # Har baar AI ko yaad dilayenge ki wo kaun hai
        system_instruction = {
            "role": "system", 
            "content": "You are Dev, a helpful assistant. You speak in Hinglish (Hindi+English). Answer ONLY what is asked. Keep answers short and direct. Do not hallucinate."
        }
        
        messages = [system_instruction] + history
        
        # --- LOGIC CONTROL ---
        # temperature=0.5 matlab "Creativity Kam, Accuracy Zyada"
        completion = client.chat_completion(
            model=Config.MODEL_ID, 
            messages=messages, 
            max_tokens=150,
            temperature=0.5 
        )
        
        reply = completion.choices[0].message.content
        
        # Assistant ka reply save karein
        history.append({"role": "assistant", "content": reply})
        session['history'] = history
        
        return jsonify({"reply": reply})
        
    except Exception as e:
        print(f"Error: {e}")
        return jsonify({"reply": "Maaf kijiye, main samajh nahi paya. Dobara boliye."})

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 8000))
    app.run(host='0.0.0.0', port=port)
    
