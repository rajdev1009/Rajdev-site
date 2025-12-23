import os

class Config:
    # Hugging Face Token ab 'HF_TOKEN' naam ke variable se aayegi
    HF_TOKEN = os.environ.get("HF_TOKEN", "YAHAN_APNA_TOKEN_PASTE_KAREIN")
    
    # Hum Llama 3.2 model use karenge jo 2025 ke liye best aur fast hai
    MODEL_ID = "meta-llama/Llama-3.2-3B-Instruct"
    
    # AI ki personality setup (Waisa hi jaisa aapne kaha tha)
    SYSTEM_INSTRUCTION = (
        "Aap Raj ke personal assistant hain. Aap hamesha Raj ki taraf se baat karenge. "
        "Aap kabhi bhi ye nahi bolenge ki aap ek AI model ya LLM hain. "
        "Aapka main kaam news dena aur Raj ke baare mein batana hai. "
        "Tum Lumding Assam se ho tumhara naam: 'Dev ho Tum'"
    )
    
