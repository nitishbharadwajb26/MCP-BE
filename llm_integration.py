import json
import requests

OLLAMA_URL = "http://localhost:11434/api/generate"

# prompt: str

def call_mistral(prompt: str) -> dict:
    import requests
    OLLAMA_URL = "http://localhost:11434/api/generate"

    system_prompt = """
You are a classifier and extractor.
Task:
1. Check if the user prompt is about creating a user or listing users.
2. If it's "create user", extract user details (id, name, email, phone, address) if present.
3. Return ONLY JSON in this format:

{
  "create_user": true/false,
  "list_user": true/false,
  "data": {
    "id": "",
    "name": "",
    "email": "",
    "phone": "",
    "address": ""
  }
}
"""
    payload = {
        "model": "mistral",
        "prompt": f"{system_prompt}\n\nUser Prompt: {prompt}",
        "stream": False
    }

    response = requests.post(OLLAMA_URL, json=payload)
    response.raise_for_status()
    result_text = response.json()["response"]

    # Parse JSON from LLM output
    try:
        parsed = json.loads(result_text)
    except Exception:
        start = result_text.find("{")
        end = result_text.rfind("}")
        parsed = json.loads(result_text[start:end+1])

    return parsed
