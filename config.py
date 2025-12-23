import os

class Config:
    HF_TOKEN = os.environ.get("HF_TOKEN", "YAHAN_APNA_TOKEN_PASTE_KAREIN")
    MODEL_ID = "meta-llama/Llama-3.2-3B-Instruct"
    
    # Updated Personality
    SYSTEM_INSTRUCTION = (
        "Aap Raj ke Assistant hain. "
        "Professional rahein aur short answers dein. "
        "Apni location (Lumding) ya personal details tabhi batayein jab koi specifically pooche. "
        "Har message mein 'Assistant' ya 'Raj' ka naam lena zaroori nahi hai. "
        "Aapka main kaam news dena aur sawalon ke jawab dena hai."
    )
    
