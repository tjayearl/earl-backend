# services/openai_service.py

import os
from dotenv import load_dotenv
import openai  # ✅ Correct import

load_dotenv()

openai.api_key = os.getenv("OPENAI_API_KEY")  # ✅ Set the API key for openai

def ask_e_a_r_l(prompt):
    try:
        response = openai.ChatCompletion.create(  # ✅ Use openai.ChatCompletion.create
            model="gpt-4o",  # or "gpt-3.5-turbo"
            messages=[{"role": "user", "content": prompt}]
        )
        return response.choices[0].message["content"]  # ✅ Safely access content
    except Exception as e:
        return f"Error: {str(e)}"

