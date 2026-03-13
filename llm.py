import os
from groq import Groq
from dotenv import load_dotenv

load_dotenv()

def get_feedback(word: str, idiom: str, user_sentence: str) -> str:
    client = Groq(api_key=os.getenv("GROQ_API_KEY"))
    
    prompt = f"""You are an English language tutor. 
The student was given:
- Word: "{word}"
- Idiom: "{idiom}"

They wrote this sentence: "{user_sentence}"

Check if they used both the word and idiom correctly and naturally.
Give brief, encouraging feedback in Russian. Max 3-4 sentences."""

    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[{"role": "user", "content": prompt}]
    )
    return response.choices[0].message.content