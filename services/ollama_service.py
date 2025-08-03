import requests

OLLAMA_URL = "http://localhost:11434/api/generate"  # Docker Ollama endpoint

def ask_ollama(prompt: str) -> str:
    """
    Sends a prompt to Ollama and returns the generated text.
    """
    try:
        payload = {
            "model": "llama3",  # or "mistral", "gemma", etc.
            "prompt": prompt,
            "stream": False
        }
        response = requests.post(OLLAMA_URL, json=payload, timeout=120)

        if response.status_code == 200:
            data = response.json()
            return data.get("response", "").strip()
        else:
            return f"Ollama error: {response.status_code} - {response.text}"

    except requests.exceptions.ConnectionError:
        return "E.A.R.L. could not connect to the AI server."
    except Exception as e:
        return f"E.A.R.L. encountered an error: {str(e)}"

