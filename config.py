import os

class Config:
    # API key Hugging Face se aayegi (Ise Koyeb Environment Variable mein bhi dalein)
    HF_TOKEN = os.environ.get("HF_TOKEN", "YAHAN_APNA_HUGGING_FACE_TOKEN_DALEIN")
    
    # Best Free AI Model
    MODEL_ID = "meta-llama/Llama-3.2-3B-Instruct"
    
    SYSTEM_INSTRUCTION = (
        "Aap Raj ke Assistant hain. Professional rahein aur short answers dein. "
        "Apni location (Lumding) tabhi batayein jab koi specifically pooche. "
        "Baat ke aakhir mein hamesha bolein: 'Bataiye aap kya janna chahte hain?'"
    )
    
