import os
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

MODES = {
    "default": "You are a helpful assistant.",
    "funny": "You are a witty and funny assistant.",
    "kid": "Explain everything like I'm five years old.",
    "motivator": "You are an energetic life coach.",
}

def ask_e_a_r_l(prompt, mode="default", model="gpt-4o"):
    try:
        system_prompt = MODES.get(mode, MODES["default"])
        response = client.chat.completions.create(
            model=model,
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": prompt}
            ]
        )
        return response.choices[0].message.content
    except Exception as e:
        return f"Error: {str(e)}"

